import discord
import config
from utils.toxicity_filter import is_tossic
from utils.file_io import WriteFile, ReadFile
from discord.ext import commands
from discord import app_commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="delete", description="Cancella un numero di messaggi.")
    @app_commands.checks.has_permissions(administrator=True)
    async def delete(self, interaction: discord.Interaction, numero: int = 1):
        await interaction.channel.purge(limit=numero + 1)
        await interaction.response.send_message(f"🧹 Ho cancellato {numero} messaggio/i!", ephemeral=True)

    @app_commands.command(name="clear_user", description="Cancella i messaggi di un utente.")
    @app_commands.checks.has_permissions(administrator=True)
    async def clear_user(self, interaction: discord.Interaction, member: discord.Member, numero: int = 1):
        def is_user(m):
            return m.author == member and not m.pinned

        deleted = await interaction.channel.purge(limit=(numero + 1), check=is_user, bulk=True)
        deleted = deleted[:numero]  # Prende solo i primi X

        await interaction.response.send_message(f"🧹 Ho eliminato {len(deleted)} messaggi di {member.display_name}.", ephemeral=True)

    @app_commands.command(name="ban", description="Banna un utente dal server.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, motivo: str = None):
        try:
            await member.ban(reason=motivo)
            msg = f"🔨 {member} è stato bannato dal server."
            if motivo:
                msg += f" Motivo: {motivo}"
            await interaction.response.send_message(msg)
        except Exception as e:
            await interaction.response.send_message(f"❌ Non posso bannare {member}. Errore: {e}", ephemeral=True)

    @app_commands.command(name="kick", description="Espelli un utente dal server.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, motivo: str = None):
        try:
            await member.kick(reason=motivo)
            msg = f"👢 {member} è stato espulso dal server."
            if motivo:
                msg += f" Motivo: {motivo}"
            await interaction.response.send_message(msg)
        except Exception as e:
            await interaction.response.send_message(f"❌ Non posso espellere {member}. Errore: {e}", ephemeral=True)

    @app_commands.command(name="mute", description="Muta un utente.")
    @app_commands.checks.has_permissions(manage_roles=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, motivo: str = None):
        muted_role = discord.utils.get(interaction.guild.roles, name="Muted")

        if not muted_role:
            try:
                muted_role = await interaction.guild.create_role(name="Muted", reason="Ruolo per mutare utenti")
                for channel in interaction.guild.channels:
                    await channel.set_permissions(muted_role, send_messages=False, speak=False, add_reactions=False)
            except Exception as e:
                await interaction.response.send_message(f"❌ Errore creando il ruolo Muted: {e}", ephemeral=True)
                return

        if muted_role in member.roles:
            await interaction.response.send_message(f"ℹ️ {member.mention} è già mutato.", ephemeral=True)
            return

        try:
            await member.add_roles(muted_role, reason=motivo)
            msg = f"🔇 {member.mention} è stato mutato."
            if motivo:
                msg += f" Motivo: {motivo}"
            await interaction.response.send_message(msg)
        except Exception as e:
            await interaction.response.send_message(f"❌ Non posso mutare {member}. Errore: {e}", ephemeral=True)

    @app_commands.command(name="list_bans", description="Mostra la lista degli utenti bannati.")
    @app_commands.checks.has_permissions(administrator=True)
    async def list_bans(self, interaction: discord.Interaction):
        try:
            ban_entries = [entry async for entry in interaction.guild.bans()]

            if not ban_entries:
                await interaction.response.send_message("📭 Non ci sono utenti bannati.", ephemeral=True)
                return

            output = "\n".join(f"{entry.user} (ID: {entry.user.id})" for entry in ban_entries)
            if len(output) > 1900:
                output = output[:1900] + "\n... (lista troncata)"
            await interaction.response.send_message(f"📛 Utenti bannati:\n{output}", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ Non ho i permessi per vedere la lista dei bannati.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Errore ottenendo la lista dei bannati: {e}", ephemeral=True)

    @app_commands.command(name="unban", description="Sbanna un utente dal server.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, user: str):
        try:
            ban_entries = await interaction.guild.bans()
            user_name, user_discrim = None, None

            # Accetta sia ID che nome#discriminatore
            if "#" in user:
                user_name, user_discrim = user.split("#")
            else:
                # Prova a convertire in ID intero
                user_id = int(user)
                for entry in ban_entries:
                    if entry.user.id == user_id:
                        await interaction.guild.unban(entry.user)
                        await interaction.response.send_message(f"✅ Utente con ID {user_id} è stato sbannato.")
                        return
                await interaction.response.send_message(f"❌ Nessun utente bannato con ID {user_id}.", ephemeral=True)
                return

            for entry in ban_entries:
                if (entry.user.name == user_name and str(entry.user.discriminator) == user_discrim):
                    await interaction.guild.unban(entry.user)
                    await interaction.response.send_message(f"✅ Utente {entry.user} è stato sbannato.")
                    return

            await interaction.response.send_message(f"❌ Utente '{user}' non trovato tra i bannati.", ephemeral=True)
        except ValueError:
            await interaction.response.send_message("❌ ID utente non valido. Usa ID numerico o nome#discriminatore.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Errore durante lo sbanno: {e}", ephemeral=True)

    @app_commands.command(name="add", description="Aggiungi una parola alla lista ban.")
    @app_commands.checks.has_permissions(administrator=True)
    async def add(self, interaction: discord.Interaction, parola: str):
        parola = parola.lower()
        parole = ReadFile(config.JSON_BANNED)
        if parola in parole:
            await interaction.response.send_message(f"⚠️ La parola `{parola}` è già nella lista.", ephemeral=True)
            return
        parole.append(parola)
        WriteFile(config.JSON_BANNED, parole)
        await interaction.response.send_message(f"✅ Parola `{parola}` aggiunta con successo.")

    @app_commands.command(name="rem", description="Rimuovi una parola dalla lista ban.")
    @app_commands.checks.has_permissions(administrator=True)
    async def rem(self, interaction: discord.Interaction, parola: str):
        parola = parola.lower()
        parole = ReadFile(config.JSON_BANNED)
        if parola not in parole:
            await interaction.response.send_message(f"⚠️ La parola `{parola}` non è nella lista.", ephemeral=True)
            return
        parole.remove(parola)
        WriteFile(config.JSON_BANNED, parole)
        await interaction.response.send_message(f"✅ Parola `{parola}` rimossa con successo.")

    @app_commands.command(name="provai", description="Testa la tossicità di una parola.")
    @app_commands.checks.has_permissions(administrator=True)
    async def provai(self, interaction: discord.Interaction, parola: str):
        await interaction.response.send_message(is_tossic(parola), ephemeral=True)

    @app_commands.command(name="info-user", description="Restituisce le informazioni di un utente.")
    @app_commands.checks.has_permissions(administrator=True)
    async def info_user(self, interaction: discord.Interaction, user: discord.User):
        embed = discord.Embed(title=f"Informazioni utente {user.name}", description=f"ID: {user.id}", color=discord.Color.blue())
        embed.add_field(name="Nome", value=user.name, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Data di creazione", value=user.created_at.strftime("%d/%m/%Y"), inline=True)
        
        # Verifica se l'utente è nel server
        member = interaction.guild.get_member(user.id)
        if member:
            embed.add_field(name="Data di join", value=member.joined_at.strftime("%d/%m/%Y") if member.joined_at else "Sconosciuta", inline=True)
            embed.add_field(name="Ruoli", value=", ".join(r.mention for r in member.roles[1:]) if len(member.roles) > 1 else "Nessun ruolo", inline=True)
        
        embed.set_thumbnail(url=user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="sync", description="Sincronizza i comandi slash del bot.")
    @app_commands.checks.has_permissions(administrator=True)
    async def sync(self, interaction: discord.Interaction):
        """Sincronizza i comandi slash del bot per questo server."""
        await interaction.response.send_message("🔄 Sincronizzazione in corso...", ephemeral=True)
        
        try:
            # Prima registra i comandi hybrid manualmente
            registered_count = 0
            for cog in self.bot.cogs.values():
                for command in cog.get_commands():
                    if isinstance(command, commands.HybridCommand):
                        try:
                            existing = self.bot.tree.get_command(command.name)
                            if existing is None:
                                slash_command = discord.app_commands.Command(
                                    name=command.name,
                                    description=command.description or command.help or "Nessuna descrizione",
                                    callback=command.callback,
                                    parent=None
                                )
                                self.bot.tree.add_command(slash_command)
                                registered_count += 1
                        except Exception as e:
                            print(f"Errore registrando {command.name}: {e}")
            
            # Ora sincronizza
            synced = await self.bot.tree.sync(guild=interaction.guild)
            
            await interaction.edit_original_response(
                content=f"✅ Sincronizzazione completata!\n"
                       f"📋 Comandi registrati: {registered_count}\n"
                       f"🔄 Comandi sincronizzati: {len(synced)}"
            )
        except Exception as e:
            await interaction.edit_original_response(
                content=f"❌ Errore durante la sincronizzazione: {e}"
            )

    @app_commands.command(name="sync_global", description="Sincronizza i comandi slash globalmente (solo per sviluppatori).")
    @app_commands.checks.has_permissions(administrator=True)
    async def sync_global(self, interaction: discord.Interaction):
        """Sincronizza i comandi slash globalmente (può richiedere fino a 1 ora per propagarsi)."""
        # Verifica che l'utente sia il proprietario del bot o un amministratore
        if interaction.user.id != self.bot.owner_id:
            await interaction.response.send_message("🚫 Solo il proprietario del bot può sincronizzare globalmente.", ephemeral=True)
            return
            
        try:
            synced = await self.bot.tree.sync()
            await interaction.response.send_message(f"✅ Sincronizzazione globale completata! {len(synced)} comandi sincronizzati.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Errore durante la sincronizzazione globale: {e}", ephemeral=True)

    @app_commands.command(name="comandi_status", description="Mostra lo stato dei comandi del bot.")
    @app_commands.checks.has_permissions(administrator=True)
    async def comandi_status(self, interaction: discord.Interaction):
        """Mostra informazioni sui comandi registrati e sincronizzati."""
        embed = discord.Embed(
            title="📊 Stato Comandi Bot",
            color=discord.Color.blue()
        )
        
        # Conta i comandi hybrid
        hybrid_count = 0
        for cog in self.bot.cogs.values():
            for command in cog.get_commands():
                if isinstance(command, commands.HybridCommand):
                    hybrid_count += 1
        
        # Conta i comandi nell'albero
        tree_count = len(self.bot.tree.get_commands())
        
        embed.add_field(
            name="🔧 Comandi Hybrid",
            value=f"`{hybrid_count}` comandi definiti",
            inline=True
        )
        
        embed.add_field(
            name="🌳 Comandi nell'Albero",
            value=f"`{tree_count}` comandi registrati",
            inline=True
        )
        
        # Verifica permessi bot
        bot_member = interaction.guild.get_member(self.bot.user.id)
        if bot_member and bot_member.guild_permissions.use_slash_commands:
            perm_status = "✅ Ha permesso"
        else:
            perm_status = "❌ Senza permesso"
        
        embed.add_field(
            name="🔑 Permesso Slash Commands",
            value=perm_status,
            inline=True
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(Admin(bot))

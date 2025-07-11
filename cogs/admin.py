import discord
import config
from utils.toxicity_filter import is_tossic
from utils.file_io import WriteFile, ReadFile
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="delete")
    @commands.has_permissions(administrator=True)
    async def delete(self, ctx, numero: int = 1):
        await ctx.channel.purge(limit=numero + 1)
        conferma = await ctx.send(f"🧹 Ho cancellato {numero} messaggio/i!")
        await conferma.delete(delay=3)

    @delete.error
    async def delete_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 Solo gli admin possono usare questo comando!", delete_after=5)

    @commands.command(name="clear_user")
    @commands.has_permissions(administrator=True)
    async def clear_user(self, ctx, member: discord.Member, numero: int = 1):
        def is_user(m):
            return m.author == member and not m.pinned

        deleted = await ctx.channel.purge(limit=(numero + 1), check=is_user, bulk=True)
        deleted = deleted[:numero]  # Prende solo i primi X

        await ctx.send(f"🧹 Ho eliminato {len(deleted)} messaggi di {member.display_name}.", delete_after=5)

    @clear_user.error
    async def clear_user_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 Solo gli admin possono usare questo comando!", delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❗ Uso corretto: `!clear_user @utente numero`", delete_after=5)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("⚠️ L'utente menzionato non è valido.", delete_after=5)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, motivo: str = None):
        try:
            await member.ban(reason=motivo)
            msg = f"🔨 {member} è stato bannato dal server."
            if motivo:
                msg += f" Motivo: {motivo}"
            await ctx.send(msg)
        except Exception as e:
            await ctx.send(f"❌ Non posso bannare {member}. Errore: {e}")

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 Non hai il permesso di bannare membri.", delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❗ Uso corretto: `!ban @utente [motivo]`", delete_after=5)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("⚠️ L'utente menzionato non è valido.", delete_after=5)

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, motivo: str = None):
        try:
            await member.kick(reason=motivo)
            msg = f"👢 {member} è stato espulso dal server."
            if motivo:
                msg += f" Motivo: {motivo}"
            await ctx.send(msg)
        except Exception as e:
            await ctx.send(f"❌ Non posso espellere {member}. Errore: {e}")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 Non hai il permesso di espellere membri.", delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❗ Uso corretto: `!kick @utente [motivo]`", delete_after=5)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("⚠️ L'utente menzionato non è valido.", delete_after=5)

    @commands.command(name="mute")
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, motivo: str = None):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")

        if not muted_role:
            try:
                muted_role = await ctx.guild.create_role(name="Muted", reason="Ruolo per mutare utenti")
                for channel in ctx.guild.channels:
                    await channel.set_permissions(muted_role, send_messages=False, speak=False, add_reactions=False)
            except Exception as e:
                await ctx.send(f"❌ Errore creando il ruolo Muted: {e}")
                return

        if muted_role in member.roles:
            await ctx.send(f"ℹ️ {member.mention} è già mutato.")
            return

        try:
            await member.add_roles(muted_role, reason=motivo)
            msg = f"🔇 {member.mention} è stato mutato."
            if motivo:
                msg += f" Motivo: {motivo}"
            await ctx.send(msg)
        except Exception as e:
            await ctx.send(f"❌ Non posso mutare {member}. Errore: {e}")

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("🚫 Non hai il permesso di gestire i ruoli.", delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❗ Uso corretto: `!mute @utente [motivo]`", delete_after=5)
        elif isinstance(error, commands.BadArgument):
            await ctx.send("⚠️ L'utente menzionato non è valido.", delete_after=5)

    @commands.command(name="list_bans")
    @commands.has_permissions(administrator=True)
    async def list_bans(self, ctx):

        try:
            ban_entries = [entry async for entry in ctx.guild.bans()]

            if not ban_entries:
                await ctx.send("📭 Non ci sono utenti bannati.")
                return

            output = "\n".join(f"{entry.user} (ID: {entry.user.id})" for entry in ban_entries)
            if len(output) > 1900:
                output = output[:1900] + "\n... (lista troncata)"
            await ctx.send(f"📛 Utenti bannati:\n{output}")

        except discord.Forbidden:
            await ctx.send("❌ Non ho i permessi per vedere la lista dei bannati.")
        except Exception as e:
            await ctx.send(f"❌ Errore ottenendo la lista dei bannati: {e}")



    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, user: str):
        try:
            ban_entries = await ctx.guild.bans()
            user_name, user_discrim = None, None

            # Accetta sia ID che nome#discriminatore
            if "#" in user:
                user_name, user_discrim = user.split("#")
            else:
                # Prova a convertire in ID intero
                user_id = int(user)
                for entry in ban_entries:
                    if entry.user.id == user_id:
                        await ctx.guild.unban(entry.user)
                        await ctx.send(f"✅ Utente con ID {user_id} è stato sbannato.")
                        return
                await ctx.send(f"❌ Nessun utente bannato con ID {user_id}.")
                return

            for entry in ban_entries:
                if (entry.user.name == user_name and str(entry.user.discriminator) == user_discrim):
                    await ctx.guild.unban(entry.user)
                    await ctx.send(f"✅ Utente {entry.user} è stato sbannato.")
                    return

            await ctx.send(f"❌ Utente '{user}' non trovato tra i bannati.")
        except ValueError:
            await ctx.send("❌ ID utente non valido. Usa ID numerico o nome#discriminatore.")
        except Exception as e:
            await ctx.send(f"❌ Errore durante lo sbanno: {e}")

    @commands.command(name="add")
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, *, parola: str):
        parola = parola.lower()
        parole = ReadFile(config.JSON_BANNED)
        if parola in parole:
            await ctx.send(f"⚠️ La parola `{parola}` è già nella lista.")
            return
        parole.append(parola)
        WriteFile(config.JSON_BANNED, parole)
        await ctx.send(f"✅ Parola `{parola}` aggiunta con successo.")
    
    
    @commands.command(name="rem")
    @commands.has_permissions(administrator=True)
    async def rem(self, ctx, *, parola: str):
        parola = parola.lower()
        parole = ReadFile(config.JSON_BANNED)
        if parola not in parole:
            await ctx.send(f"⚠️ La parola `{parola}` non è nella lista.")
            return
        parole.remove(parola)
        WriteFile(config.JSON_BANNED, parole)
        await ctx.send(f"✅ Parola `{parola}` rimossa con successo.")

    @commands.command(name="provaI")
    @commands.has_permissions(administrator=True)
    async def provaI(self, ctx, *, parola: str):
        await ctx.send(is_tossic(parola))

async def setup(bot):

    await bot.add_cog(Admin(bot))

import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

# Carica le variabili ambiente PRIMA di importare config
load_dotenv()

import config

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

def register_hybrid_commands():
    """Registra manualmente i comandi hybrid nell'albero slash"""
    print("🔧 Registrazione comandi hybrid nell'albero slash...")
    
    for cog in bot.cogs.values():
        for command in cog.get_commands():
            if isinstance(command, commands.HybridCommand):
                try:
                    # Verifica se il comando è già nell'albero
                    existing = bot.tree.get_command(command.name)
                    if existing is None:
                        # Crea un comando slash dal comando hybrid
                        slash_command = discord.app_commands.Command(
                            name=command.name,
                            description=command.description or command.help or "Nessuna descrizione",
                            callback=command.callback,
                            parent=None
                        )
                        bot.tree.add_command(slash_command)
                        print(f"✅ Registrato comando slash: /{command.name}")
                    else:
                        print(f"ℹ️ Comando {command.name} già presente nell'albero")
                except Exception as e:
                    print(f"❌ Errore registrando {command.name}: {e}")

@bot.event
async def on_ready():
    print(f"✅ {bot.user} è online!")
    print(f"🆔 Bot ID: {bot.user.id}")
    print(f"📊 Connesso a {len(bot.guilds)} server")
    
    # Registra i comandi hybrid
    register_hybrid_commands()
    
    # Debug: mostra i comandi registrati
    print(f"\n🔍 Debug - Comandi registrati nell'albero:")
    for cmd in bot.tree.get_commands():
        print(f"   - {cmd.name}: {cmd.description}")
    
    # Sincronizzazione comandi slash
    print("\n🔄 Iniziando sincronizzazione comandi slash...")
    count = 0
    total_commands = 0
    
    for guild in bot.guilds:
        print(f"\n🔍 Controllando server: {guild.name} ({guild.id})")
        
        # Controlla i permessi del bot
        bot_member = guild.get_member(bot.user.id)
        if bot_member:
            print(f"   👤 Ruolo bot: {bot_member.top_role.name}")
        
        # Controlla se il bot ha il permesso per i comandi slash
        if bot_member and bot_member.guild_permissions.use_slash_commands:
            print("   ✅ Bot ha permesso 'Use Slash Commands'")
        else:
            print("   ❌ Bot NON ha permesso 'Use Slash Commands'")
        
        try:
            synced = await bot.tree.sync(guild=guild)
            print(f"✅ Server '{guild.name}' ({guild.id}): {len(synced)} comandi sincronizzati")
            total_commands += len(synced)
            count += 1
        except Exception as e:
            print(f"❌ Errore sincronizzazione per '{guild.name}' ({guild.id}): {e}")
            # Prova sincronizzazione globale come fallback
            try:
                print("   🔄 Tentativo sincronizzazione globale...")
                synced = await bot.tree.sync()
                print(f"✅ Sincronizzazione globale riuscita: {len(synced)} comandi")
                total_commands += len(synced)
                count += 1
            except Exception as e2:
                print(f"❌ Anche la sincronizzazione globale fallita: {e2}")
    
    print(f"\n🎯 Sincronizzazione completata:")
    print(f"   📋 Server processati: {count}/{len(bot.guilds)}")
    print(f"   🔧 Comandi totali sincronizzati: {total_commands}")
    
    # Mostra i comandi disponibili
    print("\n📝 Comandi disponibili:")
    for command in bot.tree.get_commands():
        print(f"   /{command.name} - {command.description or 'Nessuna descrizione'}")

@bot.event
async def on_guild_join(guild):
    print(f"🎉 Bot aggiunto al server: {guild.name} ({guild.id})")
    try:
        synced = await bot.tree.sync(guild=guild)
        print(f"✅ Comandi sincronizzati per '{guild.name}': {len(synced)} comandi")
    except Exception as e:
        print(f"❌ Errore sincronizzazione per nuovo server '{guild.name}': {e}")

async def load_cogs():
    print("📦 Caricamento cog...")
    loaded_cogs = 0
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"✅ Cog caricato: {filename}")
                loaded_cogs += 1
            except Exception as e:
                print(f"❌ Errore nel caricamento di {filename}: {e}")
    
    print(f"📊 Totale cog caricati: {loaded_cogs}")
    
    # Debug: mostra i comandi dopo il caricamento dei cog
    print(f"\n🔍 Debug - Comandi dopo caricamento cog:")
    for cmd in bot.tree.get_commands():
        print(f"   - {cmd.name}: {cmd.description}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(config.TOKEN)

asyncio.run(main())

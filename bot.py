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

@bot.event
async def on_ready():
    print(f"✅ {bot.user} è online!")
    count = 0
    for guild in bot.guilds:
        synced = await bot.tree.sync(guild=guild)
        print(f"🔄 Slash command sincronizzati per la guild {guild.name} ({guild.id}): {len(synced)}")
        count += 1
    print(f"✅ Sincronizzazione completata per {count} server.")

@bot.event
async def on_guild_join(guild):
    synced = await bot.tree.sync(guild=guild)
    print(f"🔄 Slash command sincronizzati per la nuova guild {guild.name} ({guild.id}): {len(synced)}")

async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f"✅ Cog caricato: {filename}")
            except Exception as e:
                print(f"❌ Errore nel caricamento di {filename}: {e}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(config.TOKEN)

asyncio.run(main())

from discord.ext import commands
import discord
from discord import app_commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ciao", description="Saluta l'utente.")
    async def ciao(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"Ciao {interaction.user.mention}!")

    @app_commands.command(name="comandi", description="Mostra i comandi disponibili del bot.")
    async def comandi(self, interaction: discord.Interaction):
        """Mostra una lista dei comandi disponibili."""
        embed = discord.Embed(
            title="🤖 Comandi del Bot",
            description="Ecco i comandi disponibili:",
            color=discord.Color.blue()
        )
        
        # Raggruppa i comandi per categoria
        categories = {}
        for command in self.bot.tree.get_commands():
            cog_name = command.binding.__cog_name__ if hasattr(command, 'binding') and command.binding else "Generale"
            if cog_name not in categories:
                categories[cog_name] = []
            categories[cog_name].append(command)
        
        for category, commands_list in categories.items():
            if commands_list:
                commands_text = ""
                for cmd in commands_list:
                    desc = cmd.description or "Nessuna descrizione"
                    commands_text += f"• `/{cmd.name}` - {desc}\n"
                embed.add_field(
                    name=f"📁 {category}",
                    value=commands_text,
                    inline=False
                )
        
        embed.set_footer(text=f"Prefisso comandi: {self.bot.command_prefix}")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ping", description="Mostra la latenza del bot.")
    async def ping(self, interaction: discord.Interaction):
        """Mostra la latenza del bot."""
        latency = round(self.bot.latency * 1000)
        embed = discord.Embed(
            title="🏓 Pong!",
            description=f"Latenza: **{latency}ms**",
            color=discord.Color.green() if latency < 100 else discord.Color.orange() if latency < 200 else discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))

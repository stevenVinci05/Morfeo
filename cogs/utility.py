from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ciao(self, ctx):
        await ctx.send(f"Ciao {ctx.author.mention}!")

async def setup(bot):
    await bot.add_cog(Utility(bot))

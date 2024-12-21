import discord
from discord.ext import commands

class ServerCount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="servercount", aliases=["sc"])
    async def server_count(self, ctx):
        server_count = len(self.bot.guilds)
        embed = discord.Embed(
            title="Server Count", 
            description=f"The bot is in a total of **{server_count} servers**."
            )
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(ServerCount(bot))
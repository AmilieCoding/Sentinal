import discord
from discord.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", aliases=["latency"])
    async def ping(self, ctx):
        # -> Grabs the latency of the client.
        bot_latency = round(self.bot.latency * 1000)
        # -> Ping embed.
        ping_embed = discord.Embed(
            title="",
            description=f"**Pong!** Bot took `{bot_latency}ms` to respond."
        )
        await ctx.send(embed=ping_embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(PingCog(bot))

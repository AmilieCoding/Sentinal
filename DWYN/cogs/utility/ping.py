# Primitive as hell ping. Will change to a genuinely functioning system at some point.
import discord
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        # Grabs the latency of the client.
        bot_latency = round(self.client.latency* 1000)
        # Ping embed.
        ping_embed = discord.Embed(title="",description=f"**Pong!** Bot took `{bot_latency}ms` to respond.")
        
        await ctx.send(embed=ping_embed)

async def setup(bot):
    await bot.add_cog(Ping(bot))

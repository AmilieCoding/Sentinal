import discord
from discord.ext import commands
from discord import app_commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping", aliases=["latency"])
    async def ping(self, ctx):
        """Prefix command: Checks bot latency."""
        await self.send_ping(ctx)

    @app_commands.command(name="ping", description="Check the bot's latency.")
    async def ping_slash(self, interaction: discord.Interaction):
        """Slash command: Checks bot latency."""
        await self.send_ping(interaction, is_slash=True)

    async def send_ping(self, ctx_or_interaction, is_slash: bool = False):
        """Handles both prefix and slash ping commands."""
        bot_latency = round(self.bot.latency * 1000)
        ping_embed = discord.Embed(
            description=f"**Pong!** Bot took `{bot_latency}ms` to respond.",
            color=discord.Color.brand_green(),
        )

        if is_slash:
            await ctx_or_interaction.response.send_message(embed=ping_embed, ephemeral=True)
        else:
            await ctx_or_interaction.send(embed=ping_embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(PingCog(bot))

from discord.ext import commands
from discord import app_commands
import discord

class SayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    SUPPORT_SERVER_ID = 1311372303224930355
    DEVELOPER_ROLE_ID = 1311377148677980171

    @commands.command(name="say")
    async def say(self, ctx, *, message: str):
        """Prefix command: Allows developers to send messages through the bot."""
        await self.send_message(ctx, message)

    @app_commands.command(name="say", description="Send a message anonymously through the bot.")
    async def say_slash(self, interaction: discord.Interaction, message: str):
        """Slash command: Allows developers to send messages through the bot (anonymously)."""
        await self.send_message(interaction, message, is_slash=True)

    async def send_message(self, ctx_or_interaction, message: str, is_slash: bool = False):
        """Handles both prefix and slash command execution."""
        support_server = self.bot.get_guild(self.SUPPORT_SERVER_ID)
        if not support_server:
            return  # Ensure the bot is in the support server

        developer_role = discord.utils.get(support_server.roles, id=self.DEVELOPER_ROLE_ID)
        
        # Determine the author based on the command type
        if isinstance(ctx_or_interaction, commands.Context):
            author = ctx_or_interaction.author
            channel = ctx_or_interaction.channel
        else:  # Slash command
            author = ctx_or_interaction.user
            channel = ctx_or_interaction.channel  # FIX: Properly referencing channel

        member = support_server.get_member(author.id)
        if member and developer_role in member.roles:
            await channel.send(message)  # Sends message anonymously

            # Slash command: Send confirmation privately
            if is_slash:
                await ctx_or_interaction.response.send_message(
                    "The message has been sent.", ephemeral=True
                )
        else:
            embed = discord.Embed(
                description="**Access denied:** You must be a Developer to use this command.",
                color=discord.Color.orange(),
            )
            if is_slash:
                await ctx_or_interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await ctx_or_interaction.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(SayCog(bot))

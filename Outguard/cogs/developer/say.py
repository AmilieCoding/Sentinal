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
        await self.send_message(ctx, message)

    @app_commands.command(name="say", description="Send a message anonymously through the bot.")
    async def say_slash(self, interaction: discord.Interaction, message: str):
        await self.send_message(interaction, message, is_slash=True)

    @app_commands.command(name="reply", description="Reply to a message by its ID.")
    async def reply(self, interaction: discord.Interaction, message_id: str, message: str):
        # Attempt to convert the message_id to an integer
        try:
            message_id = int(message_id)
        except ValueError:
            await interaction.response.send_message(
                "Invalid message ID. Please input a valid integer.", ephemeral=True
            )
            return

        support_server = self.bot.get_guild(self.SUPPORT_SERVER_ID)
        if not support_server:
            return

        developer_role = discord.utils.get(support_server.roles, id=self.DEVELOPER_ROLE_ID)
        author = interaction.user
        member = support_server.get_member(author.id)
        if member and developer_role in member.roles:
            channel = interaction.channel

            try:
                # Attempt to fetch the message by ID
                message_to_reply = await channel.fetch_message(message_id)
                await message_to_reply.reply(message)
                await interaction.response.send_message(
                    f"Replied to the message successfully.", ephemeral=True
                )
            except discord.NotFound:
                await interaction.response.send_message("Message not found.", ephemeral=True)
            except discord.Forbidden:
                await interaction.response.send_message("I don't have permission to fetch that message.", ephemeral=True)
            except discord.HTTPException:
                await interaction.response.send_message("An error occurred while trying to fetch the message.", ephemeral=True)
        else:
            embed = discord.Embed(
                description="**Access denied:** You must be a Developer to use this command.",
                color=discord.Color.orange(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

    async def send_message(self, ctx_or_interaction, message: str, is_slash: bool = False):
        support_server = self.bot.get_guild(self.SUPPORT_SERVER_ID)
        if not support_server:
            return

        developer_role = discord.utils.get(support_server.roles, id=self.DEVELOPER_ROLE_ID)

        if isinstance(ctx_or_interaction, commands.Context):
            author = ctx_or_interaction.author
            channel = ctx_or_interaction.channel
        else:
            author = ctx_or_interaction.user
            channel = ctx_or_interaction.channel

        member = support_server.get_member(author.id)
        if member and developer_role in member.roles:
            await channel.send(message)

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

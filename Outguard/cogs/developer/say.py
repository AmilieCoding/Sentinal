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

    @app_commands.command(name="reply", description="Reply to a user's message.")
    async def reply(self, interaction: discord.Interaction, user_id: str, message: str):
        # Attempt to convert the user_id to an integer
        try:
            user_id = int(user_id)
        except ValueError:
            await interaction.response.send_message(
                "Invalid user ID. Please input a valid integer.", ephemeral=True
            )
            return

        support_server = self.bot.get_guild(self.SUPPORT_SERVER_ID)
        if not support_server:
            return

        developer_role = discord.utils.get(support_server.roles, id=self.DEVELOPER_ROLE_ID)
        author = interaction.user
        member = support_server.get_member(author.id)
        if member and developer_role in member.roles:
            user = support_server.get_member(user_id)
            if user:
                messages = await interaction.channel.history(limit=100).flatten()
                for msg in messages:
                    if msg.author.id == user_id:
                        await msg.reply(message)
                        await interaction.response.send_message(
                            f"Replied to {user.mention} successfully.", ephemeral=True
                        )
                        return

                await interaction.response.send_message("Message not found.", ephemeral=True)
            else:
                await interaction.response.send_message("User not found in this server.", ephemeral=True)
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

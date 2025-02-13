from discord.ext import commands
import discord
from discord import app_commands

class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban", aliases=["b"])
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None):
        # -> Check if a member was specified
        if not member:
            embed = discord.Embed(
                title="",
                description="**Missing member:** The correct usage is `ban <member>`.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Check if the bot has permission to ban the user
        if not ctx.guild.me.guild_permissions.ban_members:
            embed = discord.Embed(
                title="",
                description="**No permissions:** I require the `Ban Members` permission to ban users.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Check if the bot can ban the specified user (hierarchy check)
        if member.top_role >= ctx.guild.me.top_role or member == ctx.guild.owner:
            embed = discord.Embed(
                title="",
                description="**Cannot ban user:** This user has a higher or equal role than me.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Check if the moderator is trying to ban themselves
        if member == ctx.author:
            embed = discord.Embed(
                title="",
                description="**Command failed:** You cannot perform this command on yourself.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Attempt to ban the user
        try:
            await ctx.guild.ban(member)
            embed = discord.Embed(
                title="",
                description=f"**Banned:** The user {member.mention} has been `banned` from this guild.",
                color=discord.Color.brand_red(),
            )
            embed.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title="",
                description="No permissions: I require the `Ban Members` permission to ban users.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
        except discord.HTTPException as e:
            embed = discord.Embed(
                title="",
                description=f"**Ban failed:** An error occurred while trying to ban the user: {str(e)}",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)

    @app_commands.command(name="ban", description="Bans a member from the guild.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def slash_ban(self, interaction: discord.Interaction, member: discord.Member = None):
        # -> This works like the prefix command, but is just modified to support slash commands.
        if not member:
            embed = discord.Embed(
                title="",
                description="**Missing member:** The correct usage is `/ban <member>`.",
                color=discord.Color.orange(),
            )
            await interaction.response.send_message(embed=embed)
            return

        # -> Check if the bot has permission to ban the user
        if not interaction.guild.me.guild_permissions.ban_members:
            embed = discord.Embed(
                title="",
                description="**No permissions:** I require the `Ban Members` permission to ban users.",
                color=discord.Color.orange(),
            )
            await interaction.response.send_message(embed=embed)
            return

        # -> Check if the bot can ban the specified user (hierarchy check)
        if member.top_role >= interaction.guild.me.top_role or member == interaction.guild.owner:
            embed = discord.Embed(
                title="",
                description="**Cannot ban user:** This user has a higher or equal role than me.",
                color=discord.Color.orange(),
            )
            await interaction.response.send_message(embed=embed)
            return

        # -> Check if the moderator is trying to ban themselves
        if member == interaction.user:
            embed = discord.Embed(
                title="",
                description="**Command failed:** You cannot perform this command on yourself.",
                color=discord.Color.orange(),
            )
            await interaction.response.send_message(embed=embed)
            return

        # -> Attempt to ban the user
        try:
            await interaction.guild.ban(member)
            embed = discord.Embed(
                title="",
                description=f"**Banned:** The user {member.mention} has been `banned` from this guild.",
                color=discord.Color.brand_red(),
            )
            embed.set_footer(text=f"Moderator: {interaction.user}", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title="",
                description="No permissions: I require the `Ban Members` permission to ban users.",
                color=discord.Color.orange(),
            )
            await interaction.response.send_message(embed=embed)
        except discord.HTTPException as e:
            embed = discord.Embed(
                title="",
                description=f"**Ban failed:** An error occurred while trying to ban the user: {str(e)}",
                color=discord.Color.orange(),
            )
            await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(BanCog(bot))
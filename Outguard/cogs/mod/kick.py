import discord
from discord.ext import commands
from discord import app_commands

class KickCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -> Prefix command
    @commands.command(name="kick", aliases=["k"])
    async def kick_prefix(self, ctx, member: discord.Member = None):
        # The logic is similar to the previous prefix command
        if not member:
            embed = discord.Embed(
                title="",
                description="**Missing member:** The correct usage is `kick <member>`.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        if not ctx.guild.me.guild_permissions.kick_members:
            embed = discord.Embed(
                title="",
                description="**No permissions:** I require the `Kick Members` permission to kick users.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        if member.top_role >= ctx.guild.me.top_role or member == ctx.guild.owner:
            embed = discord.Embed(
                title="",
                description="**Cannot kick user:** This user has a higher or equal role than me.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        if member == ctx.author:
            embed = discord.Embed(
                title="",
                description="**Command failed:** You cannot perform this command on yourself.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        try:
            await ctx.guild.kick(member)
            embed = discord.Embed(
                title="",
                description=f"**Kicked:** The user {member.mention} has been `kicked` from this guild.",
                color=discord.Color.brand_red(),
            )
            embed.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title="",
                description="**No permissions:** I require the `Kick Members` permission to kick users.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
        except discord.HTTPException as e:
            embed = discord.Embed(
                title="",
                description=f"**Kick failed:** An error occurred while trying to kick the user: {str(e)}",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)

    # -> Slash command
    @app_commands.command(name="kick", description="Kick a member from the server")
    async def kick_slash(self, interaction: discord.Interaction, member: discord.Member = None):
        if not member:
            embed = discord.Embed(
                title="",
                description="**Missing member:** The correct usage is `/kick <member>`.",
                color=discord.Color.orange(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            return

        if not interaction.guild.me.guild_permissions.kick_members:
            embed = discord.Embed(
                title="",
                description="**No permissions:** I require the `Kick Members` permission to kick users.",
                color=discord.Color.orange(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            return

        if member.top_role >= interaction.guild.me.top_role or member == interaction.guild.owner:
            embed = discord.Embed(
                title="",
                description="**Cannot kick user:** This user has a higher or equal role than me.",
                color=discord.Color.orange(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            return

        if member == interaction.user:
            embed = discord.Embed(
                title="",
                description="**Command failed:** You cannot perform this command on yourself.",
                color=discord.Color.orange(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
            return

        try:
            await interaction.guild.kick(member)
            embed = discord.Embed(
                title="",
                description=f"**Kicked:** The user {member.mention} has been `kicked` from this guild.",
                color=discord.Color.brand_red(),
            )
            embed.set_footer(text=f"Moderator: {interaction.user}", icon_url=interaction.user.avatar.url)
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except discord.Forbidden:
            embed = discord.Embed(
                title="",
                description="**No permissions:** I require the `Kick Members` permission to kick users.",
                color=discord.Color.orange(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        except discord.HTTPException as e:
            embed = discord.Embed(
                title="",
                description=f"**Kick failed:** An error occurred while trying to kick the user: {str(e)}",
                color=discord.Color.orange(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)

# -> Proper async setup function
async def setup(bot: commands.Bot):
    await bot.add_cog(KickCog(bot))

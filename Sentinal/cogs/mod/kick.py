import discord
from discord.ext import commands

class KickCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -> Example command: kick
    @commands.command(name="kick", aliases=["k"])
    async def kick(self, ctx, member: discord.Member = None):
        # -> Check if a member was specified
        if not member:
            embed = discord.Embed(
                title="",
                description="**Missing member:** The correct usage is `kick <member>`.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Check if the bot has permission to kick the user
        if not ctx.guild.me.guild_permissions.kick_members:
            embed = discord.Embed(
                title="",
                description="**No permissions:** I require the `Kick Members` permission to kick users.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Check if the bot can kick the specified user (hierarchy check)
        if member.top_role >= ctx.guild.me.top_role or member == ctx.guild.owner:
            embed = discord.Embed(
                title="",
                description="**Cannot kick user:** This user has a higher or equal role than me.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Check if the moderator is trying to kick themselves
        if member == ctx.author:
            embed = discord.Embed(
                title="",
                description="**Command failed:** You cannot perform this command on yourself.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Attempt to kick the user
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
                description=f"**Ban failed:** An error occurred while trying to kick the user: {str(e)}",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)

# -> Proper async setup function
async def setup(bot: commands.Bot):
    await bot.add_cog(KickCog(bot))

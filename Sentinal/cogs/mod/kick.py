import discord
from discord.ext import commands

class KickCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -> Example command: kick
    @commands.command(name="kick")
    async def kick(self, ctx, member: discord.Member = None):
        # -> Check if a member was specified
        if not member:
            embed = discord.Embed(
                title="Missing Member",
                description="You need to specify a user to kick. Please mention a user.",
                colour=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)
            return

        # -> Check if the bot has permission to kick the user
        if not ctx.guild.me.guild_permissions.kick_members:
            embed = discord.Embed(
                title="Insufficient Permissions",
                description="I don't have permission to kick users in this server.",
                colour=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)
            return

        # -> Check if the bot can kick the specified user (hierarchy check)
        if member.top_role >= ctx.guild.me.top_role or member == ctx.guild.owner:
            embed = discord.Embed(
                title="Cannot Kick User",
                description="I cannot kick this user. They have a higher or equal role than me.",
                colour=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)
            return

        # -> Check if the moderator is trying to kick themselves
        if member == ctx.author:
            embed = discord.Embed(
                title="Action Not Allowed",
                description="You cannot kick yourself.",
                colour=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)
            return

        # -> Attempt to kick the user
        try:
            await ctx.guild.kick(member)
            embed = discord.Embed(
                title="User Kicked",
                description=f"The user {member.mention} has been successfully kicked from this guild.",
                colour=discord.Color.brand_green()
            )
            embed.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title="Insufficient Permissions",
                description="I don't have the required permissions to kick this user.",
                colour=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)
        except discord.HTTPException as e:
            embed = discord.Embed(
                title="Kick Failed",
                description=f"An error occurred while trying to kick the user: {str(e)}",
                colour=discord.Color.orange()
            )
            await ctx.send(embed=embed)

# -> Proper async setup function
async def setup(bot: commands.Bot):
    await bot.add_cog(KickCog(bot))

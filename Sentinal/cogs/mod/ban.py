from discord.ext import commands
import discord

class BanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member = None):
        # Check if a member was specified
        if not member:
            embed = discord.Embed(
                title="Missing Member",
                description="You need to specify a user to ban. Please mention a user.",
                colour=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)
            return

        # Check if the bot has permission to ban the user
        if not ctx.guild.me.guild_permissions.ban_members:
            embed = discord.Embed(
                title="Insufficient Permissions",
                description="I don't have permission to ban users in this server.",
                colour=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)
            return

        # Check if the bot can ban the specified user (hierarchy check)
        if member.top_role >= ctx.guild.me.top_role or member == ctx.guild.owner:
            embed = discord.Embed(
                title="Cannot Ban User",
                description="I cannot ban this user. They have a higher or equal role than me.",
                colour=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)
            return

        # Check if the moderator is trying to ban themselves
        if member == ctx.author:
            embed = discord.Embed(
                title="Action Not Allowed",
                description="You cannot ban yourself.",
                colour=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)
            return

        # Attempt to ban the user
        try:
            await ctx.guild.ban(member)
            embed = discord.Embed(
                title="User Banned",
                description=f"The user {member.mention} has been successfully banned from this guild.",
                colour=discord.Color.brand_green()
            )
            embed.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title="Insufficient Permissions",
                description="I don't have the required permissions to ban this user.",
                colour=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)
        except discord.HTTPException as e:
            embed = discord.Embed(
                title="Ban Failed",
                description=f"An error occurred while trying to ban the user: {str(e)}",
                colour=discord.Color.orange()
            )
            await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(BanCog(bot))

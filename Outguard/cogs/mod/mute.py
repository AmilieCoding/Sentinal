import discord
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import asyncio
from discord.utils import utcnow

class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def timeout(self, ctx, member: discord.Member, duration: str = None, *, reason: str = None):
        
        # -> Check if user can be timed out
        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(
                title="",
                description="**Error:** You cannot timeout someone with a higher or equal role.",
                color=discord.Color.orange()
            )
            return await ctx.send(embed=embed)

        # -> Convert duration string to timedelta
        if duration:
            try:
                unit = duration[-1].lower()
                amount = int(duration[:-1])
                
                if unit == 's':
                    delta = timedelta(seconds=amount)
                elif unit == 'm':
                    delta = timedelta(minutes=amount)
                elif unit == 'h':
                    delta = timedelta(hours=amount)
                elif unit == 'd':
                    delta = timedelta(days=amount)
                else:
                    raise ValueError
            except ValueError:
                embed = discord.Embed(
                    title="",
                    description="**Invalid format:** Use number + s/m/h/d\nExample: 30s, 5m, 1h, 7d",
                    color=discord.Color.orange()
                )
                return await ctx.send(embed=embed)
        else:
            delta = timedelta(minutes=5)  # -> Default timeout duration

        try:
            # -> Apply timeout
            await member.timeout(delta, reason=reason)
            
            embed = discord.Embed(
                title="",
                description=f"**Timed out:** {member.mention} has been `timed` out",
                color=discord.Color.brand_red(),
                timestamp=datetime.utcnow()
            )
            embed.add_field(name="Duration", value=duration or "5 minutes")
            if reason:
                embed.add_field(name="Reason", value=reason)
            embed.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar.url)
            
            await ctx.send(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title="",
                description="**No permissions:** I do not have permission to timeout this member.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)

    @app_commands.command(name="timeout", description="Timeout a member for a specified duration")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout_slash(self, interaction: discord.Interaction, member: discord.Member, duration: str, reason: str = None):
        # Convert the command to work with slash commands
        ctx = await self.bot.get_context(interaction)
        await self.timeout(ctx, member, duration, reason=reason)

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def untimeout(self, ctx, member: discord.Member, *, reason: str = None):
        
        # -> Check if user can be untimed out
        if member.top_role >= ctx.author.top_role:
            embed = discord.Embed(
                title="",
                description="**Error:** You cannot untimeout someone with a higher or equal role.",
                color=discord.Color.orange()
            )
            return await ctx.send(embed=embed)

        try:
            # -> Remove timeout
            await member.timeout(None, reason=reason)
            
            embed = discord.Embed(
                title="",
                description=f"**Timeout removed:** {member.mention} has been `untimed` out.",
                color=discord.Color.brand_green(),
                timestamp=datetime.utcnow()
            )
            if reason:
                embed.add_field(name="Reason", value=reason)
            embed.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar.url)
            
            await ctx.send(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title="",
                description="**No permissions:** I do not have permission to remove timeout from this member.",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)

    @app_commands.command(name="untimeout", description="Remove timeout from a member.")
    @app_commands.checks.has_permissions(moderate_members=True)
    async def untimeout_slash(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):
        # -> Convert the command to work with slash commands
        ctx = await self.bot.get_context(interaction)
        await self.untimeout(ctx, member, reason=reason)

async def setup(bot):
    await bot.add_cog(Mute(bot))

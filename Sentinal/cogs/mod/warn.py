import discord
from discord.ext import commands
import json
import os
import uuid

class WarnSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.warn_data_path = "warnings.json"

        # -> Load warnings from the JSON file.
        if not os.path.exists(self.warn_data_path):
            with open(self.warn_data_path, "w") as f:
                json.dump({}, f)
        with open(self.warn_data_path, "r") as f:
            self.warnings = json.load(f)

    def save_warnings(self):
        with open(self.warn_data_path, "w") as f:
            json.dump(self.warnings, f, indent=4)

    @commands.command(name="warn", aliases=["w"])
    @commands.has_permissions(manage_messages=True)
    async def warn(self, ctx, member: discord.Member, *, reason: str):
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        if not member:
            embed = discord.Embed(
                title="",
                description="**Missing member:** The correct usage is `warn <member>`.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Ensure the guild and user entries exist in warnings.
        if guild_id not in self.warnings:
            self.warnings[guild_id] = {}
        if user_id not in self.warnings[guild_id]:
            self.warnings[guild_id][user_id] = []

        # -> Generate a unique code for the warning.
        # -> Shorten UUID to 8 characters.
        warn_code = str(uuid.uuid4())[:8]

        # -> Add the warning.
        self.warnings[guild_id][user_id].append({"code": warn_code, "reason": reason})
        self.save_warnings()

        embed = discord.Embed(
            title="User Warned",
            description=f"**Warned:** User {member.mention} has been `warned`.",
            color=discord.Color.brand_red(),
        )
        embed.add_field(name="Reason", value=reason, inline=True)
        embed.set_footer(text=f"Moderator: {ctx.author} • Warning Code: {warn_code}", icon_url=ctx.author.avatar.url)
        

        await ctx.send(embed=embed)

    @commands.command(name="warnings", aliases=["warns"])
    @commands.has_permissions(manage_messages=True)
    async def warnings(self, ctx, member: discord.Member):
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        if guild_id in self.warnings and user_id in self.warnings[guild_id]:
            user_warnings = self.warnings[guild_id][user_id]
            if user_warnings:
                warning_list = "\n".join(f"`{warning['code']}`: {warning['reason']}" for warning in user_warnings)
                embed = discord.Embed(
                    title="User Warnings",
                    description=f"**User warning list:** {member.mention}:",
                    color=discord.Color.orange(),
                )
                embed.add_field(name="Warnings", value=warning_list, inline=False)
            else:
                embed = discord.Embed(
                    title="",
                    description=f"**No warnings:** {member.mention} has no warnings.",
                    color=discord.Color.orange(),
                )
        else:
            embed = discord.Embed(
                title="",
                description=f"**No warnings:** {member.mention} has no warnings.",
                color=discord.Color.orange(),
            )

        await ctx.send(embed=embed)

    @commands.command(name="clearwarnings", aliases=["clearwarns"])
    @commands.has_permissions(manage_messages=True)
    async def clearwarnings(self, ctx, member: discord.Member):
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        if guild_id in self.warnings and user_id in self.warnings[guild_id]:
            self.warnings[guild_id][user_id] = []
            self.save_warnings()
            embed = discord.Embed(
                title="Warnings Cleared",
                description=f"**Warnings cleared:** All warnings for {member.mention} have been deleted.",
                color=discord.Color.brand_green(),
            )
        else:
            embed = discord.Embed(
                title="No Warnings Found",
                description=f"**No warnings found:** {member.mention} has no warnings to clear.",
                color=discord.Color.orange(),
            )

        await ctx.send(embed=embed)

    @commands.command(name="delwarn", aliases=["deletewarn"])
    @commands.has_permissions(manage_messages=True)
    async def delwarn(self, ctx, member: discord.Member, code: str):
        guild_id = str(ctx.guild.id)
        user_id = str(member.id)

        # -> Check if guild and user exist in the warnings.
        if guild_id in self.warnings and user_id in self.warnings[guild_id]:
            user_warnings = self.warnings[guild_id][user_id]

            # -> Try to find and remove the warning by its code.
            for warning in user_warnings:
                if warning["code"] == code:
                    user_warnings.remove(warning)
                    self.save_warnings()

                    # -> Success embed.
                    embed = discord.Embed(
                        title="",
                        description=f"**Warning deleted:** Warning `{code}` for {member.mention} has been deleted.",
                        color=discord.Color.brand_red(),
                    )
                    await ctx.send(embed=embed)
                    return

            # -> If the code wasn't found.
            embed = discord.Embed(
                title="Warning Not Found",
                description=f"**Code not found:** Warning code `{code}` not found found for {member.mention}.",
                color=discord.Color.orange(),
            )
        else:
            # -> If no warnings exist for the user.
            embed = discord.Embed(
                title="",
                description=f"**No warnings:** {member.mention} has no warnings.",
                color=discord.Color.orange(),
            )

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(WarnSystem(bot))

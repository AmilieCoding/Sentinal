import discord
from discord.ext import commands

VIP_ROLE_NAME = 'VIP'  # -> Name of the VIP role
AUTHORIZED_ROLE_NAME = 'Developers'  # -> Name of the role authorized to use the command

class VIPManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vip(self, ctx, member_id: int):
        # -> Find the target member and their guild
        target_member = None
        target_guild = None

        for guild in self.bot.guilds:
            try:
                member = await guild.fetch_member(member_id)
                if member:
                    target_member = member
                    target_guild = guild
                    break
            except discord.NotFound:
                continue

        if not target_member:
            embed = discord.Embed(
                title="",
                description="**Error:** The specified member was not found in any guild that the bot can access.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Check if the invoking user has the authorized role in the target guild
        invoking_user = target_guild.get_member(ctx.author.id)
        if not invoking_user:
            embed = discord.Embed(
                title="",
                description="**Error:** You are not a member of the target guild.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        authorized_role = discord.utils.get(invoking_user.roles, name=AUTHORIZED_ROLE_NAME)
        if not authorized_role:
            embed = discord.Embed(
                title="",
                description="**Access denied:** You must have the 'Developers' role in the target guild to use this command.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Fetch the VIP role in the target guild
        vip_role = discord.utils.get(target_guild.roles, name=VIP_ROLE_NAME)
        if not vip_role:
            embed = discord.Embed(
                title="",
                description=f"**Role not found:** The role '{VIP_ROLE_NAME}' does not exist in `{target_guild.name}`.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Attempt to assign the VIP role
        try:
            await target_member.add_roles(vip_role)
            embed = discord.Embed(
                title="",
                description=f"**Successfully assigned:** The VIP role has been added to {target_member.mention} in `{target_guild.name}`.",
                color=discord.Color.brand_green(),
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title="",
                description=f"**Permission error:** I do not have permission to assign roles in `{target_guild.name}`.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
        except discord.HTTPException as e:
            embed = discord.Embed(
                title="",
                description=f"**Error:** An error occurred: {e}",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(VIPManager(bot))

import discord
from discord.ext import commands

SUPPORT_SERVER_ID = 1311372303224930355  # Replace with your support server's ID
AUTHORIZED_ROLE_NAME = 'Developers'  # -> Name of the role authorized to use the command
VIP_ROLE_NAME = 'VIP'  # -> Name of the VIP role to be assigned

class VIPManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def vip(self, ctx, member_id: int):
        # -> Check if the command is executed in the support server
        if ctx.guild.id != SUPPORT_SERVER_ID:
            embed = discord.Embed(
                title="",
                description="**Error:** This command can only be executed in the support server.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Find the target member in the support server
        target_member = None
        for member in ctx.guild.members:
            if member.id == member_id:
                target_member = member
                break

        if not target_member:
            embed = discord.Embed(
                title="",
                description="**Error:** The specified member was not found in the support server.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Get the invoking user in the support server
        invoking_user = ctx.author
        if not invoking_user:
            embed = discord.Embed(
                title="",
                description="**Error:** Could not find the invoking user in the support server.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Check if the invoking user has the authorized role in the support server
        authorized_role = discord.utils.find(
            lambda r: r.name.lower() == AUTHORIZED_ROLE_NAME.lower(),
            invoking_user.roles
        )
        if not authorized_role:
            embed = discord.Embed(
                title="",
                description="**Access denied:** You must have the 'Developers' role in the support server to use this command.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Fetch the VIP role in the support server
        vip_role = discord.utils.get(ctx.guild.roles, name=VIP_ROLE_NAME)
        if not vip_role:
            embed = discord.Embed(
                title="",
                description=f"**Role not found:** The role '{VIP_ROLE_NAME}' does not exist in the support server.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Attempt to assign the VIP role
        try:
            await target_member.add_roles(vip_role)
            embed = discord.Embed(
                title="",
                description=f"**Successfully assigned:** The VIP role has been added to {target_member.mention}.",
                color=discord.Color.brand_green(),
            )
            await ctx.send(embed=embed)
        except discord.Forbidden:
            embed = discord.Embed(
                title="",
                description=f"**Permission error:** I do not have permission to assign roles in the support server.",
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

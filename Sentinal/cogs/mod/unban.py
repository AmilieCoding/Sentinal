from discord.ext import commands
import discord

class UnbanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unban", aliases=["ub"])
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, identifier: str = None):
        # -> Check if an identifier (username or ID) was provided
        if not identifier:
            embed = discord.Embed(
                title="",
                description="**Missing member/ID:** The correct usage is `ban <member/ID>`",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        try:
            # -> Handle identifier as a numeric user ID.
            if identifier.isdigit():
                user_id = int(identifier)
                async for ban_entry in ctx.guild.bans():
                    if ban_entry.user.id == user_id:
                        await ctx.guild.unban(ban_entry.user)
                        embed = discord.Embed(
                            title="",
                            description=f"**Unbanned:** The user {ban_entry.user} has been `unbanned` from this guild.",
                            color=discord.Color.brand_green(),
                        )
                        embed.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar.url)
                        await ctx.send(embed=embed)
                        return

            # -> Handle identifier as a username.
            else:
                username = identifier
                async for ban_entry in ctx.guild.bans():
                    if ban_entry.user.name == username:
                        await ctx.guild.unban(ban_entry.user)
                        embed = discord.Embed(
                            title="",
                            description=f"**Unbanned:** The user {ban_entry.user} has been `unbanned` from this guild.",
                            color=discord.Color.brand_green(),
                        )
                        embed.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar.url)
                        await ctx.send(embed=embed)
                        return

            # -> If no user was found.
            embed = discord.Embed(
                title="",
                description=f"**User not found:** No banned user matching `{identifier}` was found.",
                color=discord.Color.orange(),                
            )
            await ctx.send(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title="",
                description="**No permissions:** I require the `Ban Members` permission to unban users.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="",
                description=f"**Error:** An unexpected error occurred: {str(e)}",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(UnbanCog(bot))

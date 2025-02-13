from discord.ext import commands
import discord

class ForceBanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="forceban", aliases=["fb"])
    @commands.has_permissions(ban_members=True)
    async def forceban(self, ctx, user_id: int = None): 
        # -> Check if the user ID is provided
        if not user_id:
            embed = discord.Embed(
                title="",
                description="**Missing userID:** The correct usage is `ban <ID>`.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        # -> Check if the bot has permission to ban members
        if not ctx.guild.me.guild_permissions.ban_members:
            embed = discord.Embed(
                title="",
                description="**No permissions:** I require the `Ban Members` permission to ban users.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        try:
            # -> Forceban the user by ID.
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.ban(user)

            # -> Send success message
            embed = discord.Embed(
                title="",
                description=f"**Forcebanned:** ID `{user_id}` has been `forcebanned` from this guild.",
                color=discord.Color.brand_red(),
            )
            embed.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

        except discord.NotFound:
            # -> User not found
            embed = discord.Embed(
                title="",
                description=f"**User not found:** No user found with the ID `{user_id}`.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)

        except discord.Forbidden:
            # -> Permissions issue
            embed = discord.Embed(
                title="",
                description="**No permissions:** I require the `Ban Members` permission to ban users.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)

        except discord.HTTPException as e:
            # -> HTTP exception handling
            embed = discord.Embed(
                title="",
                description=f"**Forceban failed:** An error occurred while trying to forceban the user: {str(e)}",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)

        except Exception as e:
            # -> Catch all other exceptions
            embed = discord.Embed(
                title="",
                description=f"**Error:** An unexpected error occurred: {str(e)}",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)

# -> Add the cog to the bot
async def setup(bot: commands.Bot):
    await bot.add_cog(ForceBanCog(bot))


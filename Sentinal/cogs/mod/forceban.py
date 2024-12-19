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
                title="Missing User ID",
                description="You need to specify a user ID to forceban.",
            )
            await ctx.send(embed=embed)
            return

        # -> Check if the bot has permission to ban members
        if not ctx.guild.me.guild_permissions.ban_members:
            embed = discord.Embed(
                title="Insufficient Permissions",
                description="I don't have permission to ban users in this server.",
            )
            await ctx.send(embed=embed)
            return

        try:
            # -> Forceban the user by ID.
            user = await self.bot.fetch_user(user_id)
            await ctx.guild.ban(user)

            # -> Send success message
            embed = discord.Embed(
                title="User Forcebanned",
                description=f"ID `{user_id}` has been successfully forcebanned from this guild.",
            )
            embed.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

        except discord.NotFound:
            # -> User not found
            embed = discord.Embed(
                title="User Not Found",
                description=f"No user found with the ID `{user_id}`.",
            )
            await ctx.send(embed=embed)

        except discord.Forbidden:
            # -> Permissions issue
            embed = discord.Embed(
                title="Insufficient Permissions",
                description="I don't have the required permissions to ban this user.",
            )
            await ctx.send(embed=embed)

        except discord.HTTPException as e:
            # -> HTTP exception handling
            embed = discord.Embed(
                title="Ban Failed",
                description=f"An error occurred while trying to forceban the user: {str(e)}",
            )
            await ctx.send(embed=embed)

        except Exception as e:
            # -> Catch all other exceptions
            embed = discord.Embed(
                title="Error",
                description=f"An unexpected error occurred: {str(e)}",
            )
            await ctx.send(embed=embed)

# -> Add the cog to the bot
async def setup(bot: commands.Bot):
    await bot.add_cog(ForceBanCog(bot))


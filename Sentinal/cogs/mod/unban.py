from discord.ext import commands
import discord

class UnbanCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="unban")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, identifier: str = None):
        # -> Check if an identifier (username or ID) was provided
        if not identifier:
            embed = discord.Embed(
                title="Missing Identifier",
                description="You need to specify a user to unban using their username or user ID.",
                colour=discord.Color.brand_red()
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
                            title="User Unbanned",
                            description=f"The user `{ban_entry.user}` has been successfully unbanned.",
                            colour=discord.Color.brand_green()
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
                            title="User Unbanned",
                            description=f"The user `{ban_entry.user}` has been successfully unbanned.",
                            colour=discord.Color.brand_green()
                        )
                        embed.set_footer(text=f"Moderator: {ctx.author}", icon_url=ctx.author.avatar.url)
                        await ctx.send(embed=embed)
                        return

            # -> If no user was found.
            embed = discord.Embed(
                title="User Not Found",
                description=f"No banned user matching `{identifier}` was found.",
                colour=discord.Color.orange()
            )
            await ctx.send(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title="Insufficient Permissions",
                description="I don't have the required permissions to unban this user.",
                colour=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)

        except Exception as e:
            embed = discord.Embed(
                title="Error",
                description=f"An unexpected error occurred: {str(e)}",
                colour=discord.Color.brand_red()
            )
            await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(UnbanCog(bot))

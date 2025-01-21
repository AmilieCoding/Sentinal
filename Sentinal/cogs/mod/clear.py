import discord
from discord.ext import commands

class ClearCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clear", aliases=["purge"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        if amount <= 0:
            embed = discord.Embed(
                title="",
                description="**Error:** You must specify a positive number of messages to delete.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
            return

        try:
            # -> Deletion of the messages
            deleted = await ctx.channel.purge(limit=amount+1)
        
            # -> Send a confirmation message
            embed = discord.Embed(
                title="",
                description=f"**Messaged cleared:** Deleted {len(deleted)-1} message(s) in {ctx.channel.mention}.",
                color=discord.Color.brand_green(),
            )
            confirmation_message = await ctx.send(embed=embed)
        
            # -> Delete the embed after a short delay
            await confirmation_message.delete(delay=10)

        except discord.Forbidden:
            embed = discord.Embed(
                title="",
                description="**No permissions:** I require the `Manage Messages` permission to ban users.",
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

    @clear.error
    async def clear_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                title="",
                description="**Missing amount:** The correct usage is `$clear <amount>`.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="",
                description="**No permissions:** I require the `Manage Messages` permission to ban users.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="",
                description="**Error:** An unexpected error occurred.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)

# -> Proper async setup function
async def setup(bot: commands.Bot):
    await bot.add_cog(ClearCog(bot))
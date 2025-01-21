from discord.ext import commands
import discord

class SayCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -> Replace with your support server ID and Developer role ID.
    SUPPORT_SERVER_ID = 1311372303224930355
    DEVELOPER_ROLE_ID = 1311377148677980171

    @commands.command(name="say")
    async def say(self, ctx, *, message: str):
        # -> Fetch the support server.
        support_server = self.bot.get_guild(self.SUPPORT_SERVER_ID)
        developer_role = discord.utils.get(support_server.roles, id=self.DEVELOPER_ROLE_ID)

        # -> Get the user's membership in the support server
        member = support_server.get_member(ctx.author.id)
        if member and developer_role in member.roles:
            await ctx.send(message)
        else:
            # -> Embed for the access denied error.
            embed = discord.Embed(
                title="",
                description="**Access denied:** You have to be a Developer to use this command.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(SayCog(bot))
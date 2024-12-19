import discord
from discord.ext import commands

class InviteCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # -> Bot's ID and permissions integer.
        self.bot_id = '1316526920451756103'
        self.permissions = 8

    @commands.command(name="invite", aliases=["inv"])
    async def invite(self, ctx):
        # -> Generate the invite link.
        invite_url = f"https://discord.com/oauth2/authorize?client_id={self.bot_id}&permissions={self.permissions}&scope=bot%20applications.commands"

        # -> Create the embed.
        embed = discord.Embed(
            title="",
            description=f"**Invite me! [Click any of this bolded blue text to invite the bot!]({invite_url})**"
        )
        embed.add_field(name="Need an invite to our Support Server?", value="[Click here, and it'll redirect you to our server.](https://discord.gg/2q7sHEUwzX)", inline=True)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        # -> Send the embed
        await ctx.send(embed=embed)

# -> Setup function for the cog
async def setup(bot: commands.Bot):
    await bot.add_cog(InviteCommand(bot))

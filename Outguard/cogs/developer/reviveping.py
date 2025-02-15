import discord
from discord.ext import commands, tasks
from datetime import datetime, time, timezone

class RevivePing(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.daily_ping.start()

    def cog_unload(self):
        self.daily_ping.cancel()

    @tasks.loop(time=time(hour=13, minute=30, tzinfo=timezone.utc))  # 1:30 PM UTC
    async def daily_ping(self):
        GUILD_ID = 1330917905445163151 # Your server ID
        CHANNEL_ID = 1333188347807662113  # Your channel ID
        ROLE_ID = 1334958474760552601  # Your role ID

        guild = self.bot.get_guild(GUILD_ID)
        if guild:
            channel = guild.get_channel(CHANNEL_ID)
            if channel:
                role = guild.get_role(ROLE_ID)
                if role:
                    await channel.send(f"{role.mention} Rise!")

    @daily_ping.before_loop
    async def before_daily_ping(self):
        await self.bot.wait_until_ready()

async def setup(bot: commands.Bot):
    await bot.add_cog(RevivePing(bot))

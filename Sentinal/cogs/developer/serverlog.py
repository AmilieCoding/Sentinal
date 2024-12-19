import discord
from discord.ext import commands

class ServerLogger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logging_channel_id = 1319380111362883645

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        logging_channel = self.bot.get_channel(self.logging_channel_id)
        if logging_channel is None:
            print(f"Logging channel with ID {self.logging_channel_id} not found.")
            return

        guild_name = guild.name
        guild_id = guild.id
        guild_icon_url = guild.icon.url if guild.icon else None

        # -> Get total number of servers.
        total_servers = len(self.bot.guilds)

        embed = discord.Embed(
            title="Bot has joined a guild.",
            color=discord.Color.green()
        )
        embed.add_field(name="Server Name", value=guild_name, inline=False)
        embed.add_field(name="Server ID", value=guild_id, inline=False)
        embed.add_field(name="Total Servers", value=str(total_servers), inline=False)
        if guild_icon_url:
            embed.set_thumbnail(url=guild_icon_url)

        await logging_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        logging_channel = self.bot.get_channel(self.logging_channel_id)
        if logging_channel is None:
            print(f"Logging channel with ID {self.logging_channel_id} not found.")
            return

        guild_name = guild.name
        guild_id = guild.id
        guild_icon_url = guild.icon.url if guild.icon else None

        # -> Get total number of servers.
        total_servers = len(self.bot.guilds)

        embed = discord.Embed(
            title="Bot has left a guild.",
            color=discord.Color.red()
        )
        embed.add_field(name="Server Name", value=guild_name, inline=False)
        embed.add_field(name="Server ID", value=guild_id, inline=False)
        embed.add_field(name="Total Servers", value=str(total_servers), inline=False)  # Add total servers count
        if guild_icon_url:
            embed.set_thumbnail(url=guild_icon_url)

        await logging_channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ServerLogger(bot))
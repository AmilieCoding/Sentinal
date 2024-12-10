import discord
import json
from discord.ext import commands
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "config.json"

class JoinLogs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = self.load_config()

    def load_config(self):
        if CONFIG_FILE.exists():
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_config(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config, f, indent=4)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        channel_id = self.config.get(guild_id)
        if channel_id:
            channel = member.guild.get_channel(int(channel_id))
            if channel:
                await channel.send(f"Welcome {member.mention} to the server!")

    @commands.command(name="setjoinlog")
    @commands.has_permissions(administrator=True)
    async def set_join_log(self, ctx, *args):
        guild_id = str(ctx.guild.id)
        state = None
        channel = None

        for i, arg in enumerate(args):
            if arg.startswith("?s"):
                state = arg[2:].strip().lower() 
            elif arg.startswith("?c") and i + 1 < len(args):
                try:
                    channel = await commands.TextChannelConverter().convert(ctx, args[i + 1])
                except commands.BadArgument:
                    await ctx.send(f"Invalid channel: {args[i + 1]}")
                    return

        if state not in ("on", "off"):
            await ctx.send("Invalid or missing state. Use `?s on` to enable or `?s off` to disable.")
            return

        if state == "on":
            if channel is None:
                await ctx.send("Missing channel. Use `?c #channel-name` to specify the channel.")
                return

            self.config[guild_id] = channel.id
            self.save_config()
            await ctx.send(f"Join logs have been enabled for: {channel.mention}")

        elif state == "off":
            if guild_id in self.config:
                del self.config[guild_id]
                self.save_config()
                await ctx.send("Join logs have been disabled.")
            else:
                await ctx.send("Join logs are not enabled for this server.")

async def setup(bot):
    await bot.add_cog(JoinLogs(bot))

import json
from pathlib import Path

import discord
from discord.ext import commands

CONFIG_FILE = Path(__file__).parent / "config.json"


class JLFlags(commands.FlagConverter, case_insensitive=True, delimiter=" ", prefix="-"):
    state: str = commands.flag(
        name="state",
        description="Enable or disable join-logs.",
        aliases=["s"],
        default=None,  # Changed from MISSING to None
    )
    channel: discord.TextChannel | None = commands.flag(
        name="channel",
        description="Set join-logs' channel.",
        aliases=["c"],
        default=None,
    )


class JoinLogs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config: dict[str, int] = self.load_config()

    def load_config(self) -> dict[str, int]:
        """Load configuration from the JSON file."""
        if CONFIG_FILE.exists():
            with CONFIG_FILE.open("r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def save_config(self):
        """Save the current configuration to the JSON file."""
        with CONFIG_FILE.open("w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=4)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if channel_id := self.config.get(str(member.guild.id)):
            channel = member.guild.get_channel(channel_id)
            if channel and isinstance(channel, discord.TextChannel):
                await channel.send(f"Welcome {member.mention} to the server!")

    @commands.hybrid_command(name="setjoinlog")
    @commands.has_permissions(administrator=True)
    async def set_join_log(self, ctx: commands.Context[commands.Bot], *, flags: JLFlags) -> None:
        """
        Command to enable or disable join logs for the server.

        Usage:
            >setjoinlog -s on -c #channel-name
            >setjoinlog -s off
        """
        if not ctx.guild:
            await ctx.send("This command cannot be used in DMs.")
            return

        guild_id = str(ctx.guild.id)

        # Check if state is None
        if flags.state is None:
            await ctx.send("Please specify a state ('on' to enable or 'off' to disable join logs).")
            return

        # Normalize state value
        state = flags.state.lower()

        # Validate the state
        if state not in ["on", "off"]:
            await ctx.send("Invalid state. Use 'on' to enable or 'off' to disable join logs.")
            return

        if state == "on":
            # Ensure channel is specified
            if flags.channel is None:
                await ctx.send("You must specify a valid channel for join logs.")
                return

            # Try to find the specified channel
            channel = flags.channel
            if not channel:
                await ctx.send("Could not find the specified channel. Please check the channel name.")
                return

            # Set the join log channel
            self.config[guild_id] = channel.id

            await ctx.send(f"Join logs have been enabled for {channel.mention}.")

        elif state == "off":
            # Disable join logs if they were previously enabled
            if self.config.pop(guild_id, None):
                await ctx.send("Join logs have been disabled.")
            else:
                await ctx.send("Join logs were not enabled for this server.")

        # Save the configuration
        self.save_config()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(JoinLogs(bot))

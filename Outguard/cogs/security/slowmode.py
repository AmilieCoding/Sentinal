import discord
from discord.ext import commands
from discord import app_commands

class SlowmodeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # -> Traditional command (prefix-based)
    @commands.command(name="slowmode", aliases=["sm"])
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, *args):
        # -> Default values.
        seconds = 0
        channel = ctx.channel  # -> Default to current channel.
        
        # -> If two arguments are provided.
        if len(args) == 1:
            # -> Check if the first argument is a channel or seconds.
            try:
                # -> Try to interpret the first argument as a channel name.
                if args[0].startswith('#'):
                    channel_name = args[0][1:]  # Remove '#' symbol
                    channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
                    if not channel:
                        raise ValueError("Channel not found.")
                else:
                    # -> If it's not a channel name, interpret it as seconds.
                    seconds = int(args[0])
            except ValueError as e:
                embed = discord.Embed(
                    title="",
                    description=f"**Error:** {str(e)}",
                )
                await ctx.send(embed=embed)
                return

        elif len(args) == 2:
            # -> If both arguments are provided, interpret the first as channel and second as seconds.
            channel_name = args[0][1:]  # Remove '#' symbol
            channel = discord.utils.get(ctx.guild.text_channels, name=channel_name)
            seconds = int(args[1])

        # -> If channel is still None, default to current channel.
        if channel is None:
            channel = ctx.channel

        await self.apply_slowmode(ctx, channel, seconds)

    async def apply_slowmode(self, ctx_or_interaction, channel, seconds):
        # Check if the input time is valid
        if seconds < 0:
            embed = discord.Embed(
                title="",
                description="**Invalid value:** Channel slowmode cannot be a negative digit.",
                color=discord.Color.orange(),
            )
            if isinstance(ctx_or_interaction, discord.Interaction):
                await ctx_or_interaction.response.send_message(embed=embed)
            else:
                await ctx_or_interaction.send(embed=embed)
            return

        try:
            await channel.edit(slowmode_delay=seconds)

            if seconds == 0:
                description = f"**Disabled:** Slowmode has been `reset` in {channel.mention}."
            else:
                description = f"**Enabled:** Slowmode for {channel.mention} is now set to `{seconds} seconds`."

            embed = discord.Embed(
                title="",
                description=description,
                color=discord.Color.brand_green(),
            )
            
            author = ctx_or_interaction.user if isinstance(ctx_or_interaction, discord.Interaction) else ctx_or_interaction.author
            embed.set_footer(text=f"Moderator: {author}", icon_url=author.avatar.url)

            if isinstance(ctx_or_interaction, discord.Interaction):
                await ctx_or_interaction.response.send_message(embed=embed)
            else:
                await ctx_or_interaction.send(embed=embed)

        except discord.Forbidden:
            embed = discord.Embed(
                title="",
                description="**No permissions:** I require the `Manage Channel` permission to change slowmode.",
                color=discord.Color.orange(),
            )
            if isinstance(ctx_or_interaction, discord.Interaction):
                await ctx_or_interaction.response.send_message(embed=embed)
            else:
                await ctx_or_interaction.send(embed=embed)

    # -> Slash command implementation
    @app_commands.command(name="slowmode", description="Set or reset the slowmode of a channel.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def slowmode_slash(self, interaction: discord.Interaction, channel: discord.TextChannel = None, seconds: int = 0):
        # -> If no channel is provided, use the current channel
        if not channel:
            channel = interaction.channel

        await self.apply_slowmode(interaction, channel, seconds)

async def setup(bot: commands.Bot):
    await bot.add_cog(SlowmodeCog(bot))

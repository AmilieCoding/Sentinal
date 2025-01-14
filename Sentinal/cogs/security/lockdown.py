import discord
from discord.ext import commands

class LockdownCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def lockdown_channel(self, channel, reason=None, message=None, moderator=None):
        overwrite = channel.overwrites_for(channel.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(channel.guild.default_role, overwrite=overwrite, reason=reason)

        # -> Create the embed message for the locked channel.
        embed = discord.Embed(title="",
                description=f"**Channel locked:** The channel {channel.mention} has been locked down.",
                color=discord.Color.brand_red())
        embed.add_field(name="Moderator", value=moderator, inline=False)
        if message:
            embed.add_field(name="Message", value=message, inline=False)

        await channel.send(embed=embed)

    @commands.command(name="lockdown", aliases=["ld"])
    @commands.has_permissions(manage_channels=True)
    async def lockdown(self, ctx, channel: discord.TextChannel = None, *, message=None):
        # -> Default to current channel if no channel specified.
        channel = channel or ctx.channel

        try:
            # -> Lock the channel.
            await self.lockdown_channel(
                channel,
                reason=f"Lockdown initiated by {ctx.author}.",
                message=message,
                moderator=ctx.author.mention
            )

            # -> Confirmation embed sent to the invoking channel.
            embed = discord.Embed(
                title="",
                description=f"**Channel locked:** The channel {channel.mention} has been locked down.",
                color=discord.Color.brand_red()
            )
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
            await ctx.send(embed=embed)

        except Exception as e:
            # -> Error embed.
            embed = discord.Embed(
                title="",
                description=f"**Error:** An error occurred while locking down the channel: {e}",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)

    @commands.command(name="lockdownall", aliases=["ldall"])
    @commands.has_permissions(manage_channels=True)
    async def lockdownall(self, ctx, *, message=None):
        try:
            failed_channels = []

            for channel in ctx.guild.text_channels:
                try:
                    await self.lockdown_channel(
                        channel,
                        reason=f"Lockdown initiated by {ctx.author}.",
                        message=message,
                        moderator=ctx.author.mention
                    )
                except Exception:
                    failed_channels.append(channel.name)

            # -> Create the embed message for the invoking channel.
            embed = discord.Embed(
                title="",
                color=discord.Color.brand_red()
            )
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)

            if message:
                embed.add_field(name="Message", value=message, inline=False)

            if failed_channels:
                embed.add_field(
                    name="Failed Channels",
                    value=", ".join(failed_channels),
                    inline=False
                )
            else:
                description="**Lockdown all completed:** All channels have been locked."

            await ctx.send(embed=embed)

        except Exception as e:
            # -> Error embed.
            embed = discord.Embed(
                title="",
                description=f"**Error:** An error occurred while locking down all channels: {e}",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)

    async def unlock_channel(self, channel, reason=None, message=None, moderator=None):
        overwrite = channel.overwrites_for(channel.guild.default_role)
        overwrite.send_messages = None
        await channel.set_permissions(channel.guild.default_role, overwrite=overwrite, reason=reason)

        # -> Create the embed message for the unlocked channel.
        embed = discord.Embed(title="", 
            description="**Channel unlocked:** The channel has been unlocked.",
            color=discord.Color.brand_green()
            )
        embed.add_field(name="Moderator", value=moderator, inline=False)
        if message:
            embed.add_field(name="Message", value=message, inline=False)

        await channel.send(embed=embed)

    @commands.command(name="unlock", aliases=["ul"])
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None, *, message=None):
        # -> As againn, defaults to current channel if no channel specified.
        channel = channel or ctx.channel

        try:
            # -> Unlock the channel.
            await self.unlock_channel(
                channel,
                reason=f"Unlock initiated by {ctx.author}.",
                message=message,
                moderator=ctx.author.mention
            )

            # -> Confirmation embed sent to the invoking channel.
            embed = discord.Embed(
                title="",
                description=f"**Channel unlocked:** The channel has been unlocked.",
                color=discord.Color.brand_green(),
            )
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)
            await ctx.send(embed=embed)

        except Exception as e:
            # -> Error embed.
            embed = discord.Embed(
                title="",
                description=f"**Error:** An error occurred while unlocking the channel: {e}",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)

    @commands.command(name="unlockall", aliases=["ulall"])
    @commands.has_permissions(manage_channels=True)
    async def unlockall(self, ctx, *, message=None):
        try:
            failed_channels = []

            for channel in ctx.guild.text_channels:
                try:
                    await self.unlock_channel(
                        channel,
                        reason=f"Unlock initiated by {ctx.author}.",
                        message=message,
                        moderator=ctx.author.mention
                    )
                except Exception:
                    failed_channels.append(channel.name)

            # -> Create the embed message for the invoking channel.
            embed = discord.Embed(
                title="",
                color=discord.Color.brand_green()
            )
            embed.add_field(name="Moderator", value=ctx.author.mention, inline=False)

            if message:
                embed.add_field(name="Message", value=message, inline=False)

            if failed_channels:
                embed.add_field(
                    name="Failed Channels",
                    value=", ".join(failed_channels),
                    inline=False
                )
            else:
                embed.description = "**Unlock all completed:** All channels have been unlocked."

            await ctx.send(embed=embed)

        except Exception as e:
            # -> Error embed.
            embed = discord.Embed(
                title="",
                description=f"**Error:** An error occurred while unlocking all channels: {e}",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(LockdownCog(bot))
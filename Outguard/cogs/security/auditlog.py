import discord
from discord.ext import commands
from discord import app_commands
import logging
import json
import os

class auditlog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger("discord")
        self.audit_log_file = "audit_log_channels.json"
        self.audit_log_channels = self.load_audit_channels()

    def load_audit_channels(self):
        if os.path.exists(self.audit_log_file):
            with open(self.audit_log_file, 'r') as f:
                return json.load(f)
        else:
            with open(self.audit_log_file, 'w') as f:
                json.dump({}, f)
            return {}

    def save_audit_channels(self):
        with open(self.audit_log_file, 'w') as f:
            json.dump(self.audit_log_channels, f, indent=4)

    async def log_to_channel(self, guild_id: int, embed: discord.Embed):
        channel_id = self.audit_log_channels.get(str(guild_id))
        if channel_id:
            channel = self.bot.get_channel(channel_id)
            if channel:
                embed.timestamp = datetime.utcnow()
                await channel.send(embed=embed)

    @commands.command(name="setauditlog")
    @commands.has_permissions(administrator=True)
    async def set_audit_log(self, ctx, channel: discord.TextChannel = None):
        if channel:
            self.audit_log_channels[str(ctx.guild.id)] = channel.id
            self.save_audit_channels()
            embed = discord.Embed(description=f"**Audit log channel set:** Channel set to {channel.mention}.", color=discord.Color.brand_green())
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(description="**Missing channel:** Please mention a valid text channel.", color=discord.Color.orange())
            await ctx.send(embed=embed)

    @app_commands.command(name="setauditlog", description="Set the audit log channel for this server")
    @app_commands.describe(channel="The channel to set as the audit log channel")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_audit_log_slash(self, interaction: discord.Interaction, channel: discord.TextChannel):
        self.audit_log_channels[str(interaction.guild_id)] = channel.id
        self.save_audit_channels()
        embed = discord.Embed(description=f"**Audit log channel set:** Channel set to {channel.mention}.", color=discord.Color.brand_green())
        await interaction.response.send_message(embed=embed)

    # Moderation Events
    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        embed = discord.Embed(title="Member Banned", description=f"{user.mention} was banned.", color=discord.Color.red())
        embed.set_footer(text=f"User ID: {user.id}")
        await self.log_to_channel(guild.id, embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(title="Member Left/Kicked", description=f"{member.mention} left or was kicked.", color=discord.Color.orange())
        embed.set_footer(text=f"User ID: {member.id}")
        await self.log_to_channel(member.guild.id, embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(title="Member Joined", description=f"{member.mention} joined the server.", color=discord.Color.green())
        embed.set_footer(text=f"User ID: {member.id}")
        await self.log_to_channel(member.guild.id, embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            added = set(after.roles) - set(before.roles)
            removed = set(before.roles) - set(after.roles)
            embed = discord.Embed(title="Member Roles Updated", description=f"Role changes for {after.mention}", color=discord.Color.blue())
            if added:
                embed.add_field(name="Added Roles", value=", ".join(role.mention for role in added))
            if removed:
                embed.add_field(name="Removed Roles", value=", ".join(role.mention for role in removed))
            await self.log_to_channel(after.guild.id, embed)

        if before.nick != after.nick:
            embed = discord.Embed(title="Nickname Changed", color=discord.Color.blue())
            embed.add_field(name="Member", value=after.mention)
            embed.add_field(name="Before", value=before.nick or "None")
            embed.add_field(name="After", value=after.nick or "None")
            await self.log_to_channel(after.guild.id, embed)

    # Server Changes
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        embed = discord.Embed(title="Channel Created", description=f"Channel {channel.mention} was created", color=discord.Color.green())
        await self.log_to_channel(channel.guild.id, embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        embed = discord.Embed(title="Channel Deleted", description=f"Channel #{channel.name} was deleted", color=discord.Color.red())
        await self.log_to_channel(channel.guild.id, embed)

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        if before.name != after.name:
            embed = discord.Embed(title="Channel Updated", description=f"Channel renamed from #{before.name} to #{after.name}", color=discord.Color.blue())
            await self.log_to_channel(after.guild.id, embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel != after.channel:
            embed = discord.Embed(title="Voice Channel Movement", color=discord.Color.blue())
            embed.add_field(name="Member", value=member.mention)
            embed.add_field(name="Before", value=before.channel.name if before.channel else "None")
            embed.add_field(name="After", value=after.channel.name if after.channel else "None")
            await self.log_to_channel(member.guild.id, embed)

    # Message Events
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            embed = discord.Embed(title="Message Deleted", color=discord.Color.red())
            embed.add_field(name="Author", value=message.author.mention)
            embed.add_field(name="Channel", value=message.channel.mention)
            embed.add_field(name="Content", value=message.content or "No content", inline=False)
            await self.log_to_channel(message.guild.id, embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.author.bot and before.content != after.content:
            embed = discord.Embed(title="Message Edited", color=discord.Color.blue())
            embed.add_field(name="Author", value=before.author.mention)
            embed.add_field(name="Channel", value=before.channel.mention)
            embed.add_field(name="Before", value=before.content, inline=False)
            embed.add_field(name="After", value=after.content, inline=False)
            await self.log_to_channel(before.guild.id, embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(auditlog(bot))

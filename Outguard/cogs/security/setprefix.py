import discord
from discord.ext import commands
from discord import app_commands
import json
import os

class SetPrefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.prefix_file = "prefixes.json"
        if not os.path.exists(self.prefix_file):
            with open(self.prefix_file, "w") as f:
                json.dump({}, f)

    def get_prefix(self, guild_id):
        with open(self.prefix_file, "r") as f:
            prefixes = json.load(f)
        return prefixes.get(str(guild_id), "$")

    def save_prefix(self, guild_id, prefix):
        with open(self.prefix_file, "r") as f:
            prefixes = json.load(f)
        
        prefixes[str(guild_id)] = prefix
        
        with open(self.prefix_file, "w") as f:
            json.dump(prefixes, f, indent=4)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setprefix(self, ctx, new_prefix: str):
        if len(new_prefix) > 3:
            embed = discord.Embed(
                description="**Error:** Prefix cannot be longer than 3 characters!",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
            return

        self.save_prefix(ctx.guild.id, new_prefix)
        embed = discord.Embed(
            description=f"**Success:** Server prefix has been updated to: `{new_prefix}`",
            color=discord.Color.brand_green()
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="setprefix", description="Set a new prefix for the bot in this server")
    @app_commands.default_permissions(administrator=True)
    async def setprefix_slash(self, interaction: discord.Interaction, new_prefix: str):
        if len(new_prefix) > 3:
            embed = discord.Embed(
                description="**Error:** Prefix cannot be longer than 3 characters!",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        self.save_prefix(interaction.guild_id, new_prefix)
        embed = discord.Embed(
            description=f"**Success:** Server prefix has been updated to: `{new_prefix}`",
            color=discord.Color.brand_green()
        )
        await interaction.response.send_message(embed=embed)

    @setprefix.error
    async def setprefix_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description="**Access Denied:** You need administrator permissions to change the prefix!",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description="**Error:** Please specify a new prefix!",
                color=discord.Color.orange()
            )
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(SetPrefix(bot))
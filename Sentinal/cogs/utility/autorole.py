import discord
from discord.ext import commands
import json
import os

class AutoRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        # -> Ensure the JSON file exists.
        self.DATA_FILE = "autoroles.json"
        if not os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, "w") as file:
                json.dump({}, file)

        self.data = self.load_data()

    def load_data(self):
        with open(self.DATA_FILE, "r") as file:
            return json.load(file)

    def save_data(self):
        with open(self.DATA_FILE, "w") as file:
            json.dump(self.data, file, indent=4)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild_id = str(member.guild.id)
        if guild_id in self.data:
            role_id = self.data[guild_id]
            role = member.guild.get_role(role_id)
            if role:
                await member.add_roles(role)

    @commands.group(name="autorole",invoke_without_commands=True, aliases=["ar"])
    async def autorole(self, ctx):
        embed = discord.Embed(
            title="",
            description="**** Autorole commands:** Subcommands to manage the guild autorole.",
        )
        embed.add_field(name="setautorole", value="Set the auto-role for new members.", inline=False)
        embed.add_field(name="deleteautorole", value="Delete the auto-role for new members.", inline=False)
        embed.add_field(name="currentautorole", value="View the current auto-role for new members.", inline=False)
        await ctx.send(embed=embed)

    @commands.command(name="setautorole", aliases=["sar"])
    @commands.has_permissions(manage_roles=True)
    async def set_autorole(self, ctx, role: discord.Role):
        guild_id = str(ctx.guild.id)
        self.data[guild_id] = role.id
        self.save_data()

        embed = discord.Embed(
            title="",
            description=f"**Autorole set:** Autorole has been set to {role.mention} for this guild.",
            color=discord.Color.brand_green(),
        )
        await ctx.send(embed=embed)

    @commands.command(name="deleteautorole", aliases=["dar"])
    @commands.has_permissions(manage_roles=True)
    async def delete_autorole(self, ctx):
        guild_id = str(ctx.guild.id)
        if guild_id in self.data:
            del self.data[guild_id]
            self.save_data()

            embed = discord.Embed(
                title="",
                description="**Autorole deleted:** The autorole has been removed for this guild.",
                color=discord.Color.brand_green(),
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="",
                description="**No autorole set:** No autorole has been set for this guild.",
                color=discord.Color.orange(),
            )
            await ctx.send(embed=embed)

    @commands.command(name="currentautorole", aliases=["car"])
    @commands.has_permissions(manage_roles=True)
    async def list_autorole(self, ctx):
        guild_id = str(ctx.guild.id)
        if guild_id in self.data:
            role_id = self.data[guild_id]
            role = ctx.guild.get_role(role_id)

            embed = discord.Embed(
                title="",
                description=f"**Current autorole:** The current auto-role is {role.mention if role else 'Deleted Role'}.",
                color=discord.Color.brand_green(),
            )
        else:
            embed = discord.Embed(
                title="",
                description="**No autorole set:** No autorole has been set for this guild.",
                color=discord.Color.orange(),
            )
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(AutoRole(bot))
import discord
from discord.ext import commands
from discord import app_commands

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counting_channel = None
        self.start_number = 1
        self.last_user = None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.channel != self.counting_channel:
            return
        
        try:
            current_number = int(message.content.strip())
        except ValueError:
            await message.delete()
            return
        
        if current_number != self.start_number:
            await message.delete()
            return

        self.start_number = current_number + 1
        self.last_user = message.author
        await message.add_reaction("✅")

    @commands.command()
    async def setcountingchannel(self, ctx, channel: discord.TextChannel = None):
        if channel:
            self.counting_channel = channel
            embed = discord.Embed(
                title="",
                description=f"**Counting channel set:** You can start counting from `{self.start_number}`.\n\n- Text will be deleted when sent, the only allows numbers in the sequence.\n- If the number has a checkmark, it means the number has been accepted.",
                color=discord.Color.brand_green()
            )
            await channel.send(embed=embed)
            await interaction.response.send_message(f"Counting channel set to {channel.mention}.", ephemeral=True)
        else:
            await ctx.send("Please specify a channel.")

    @commands.command()
    async def setstartnumber(self, ctx, number: int):
        self.start_number = number
        embed = discord.Embed(
            title="",
            description=f"**Number set:** The counting will now start from `{self.start_number}`.",
            color=discord.Color.brand_green()
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="setcountingchannel", description="Set the counting channel for the server.")
    async def setcountingchannel_slash(self, interaction: discord.Interaction, channel: discord.TextChannel):
        self.counting_channel = channel
        embed = discord.Embed(
            title="",
            description=f"**Counting channel set:** You can start counting from `{self.start_number}`.\n\n- Text will be deleted when sent, the only allows numbers in the sequence.\n- If the number has a checkmark, it means the number has been accepted.",
            color=discord.Color.brand_green()
        )
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Counting channel set to {channel.mention}.", ephemeral=True)

    @app_commands.command(name="setstartnumber", description="Set the number to start counting from.")
    async def setstartnumber_slash(self, interaction: discord.Interaction, number: int):
        self.start_number = number
        embed = discord.Embed(
            title="",
            description=f"**Number set:** The counting will now start from `{self.start_number}`.",
            color=discord.Color.brand_green()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Counting(bot))

class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.counting_data = self.load_counting_data()

    def load_counting_data(self):
        if os.path.exists("counting_data.json"):
            with open("counting_data.json", "r") as f:
                print("Loaded counting data")
                return json.load(f)
        print("No counting data file found, starting fresh.")
        return {}

    def save_counting_data(self):
        print("Saving counting data...")
        with open("counting_data.json", "w") as f:
            json.dump(self.counting_data, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        
        server_id = str(message.guild.id)
        if server_id not in self.counting_data:
            print(f"No data for server {server_id}, ignoring message.")
            return

        counting_channel = self.counting_data[server_id].get("counting_channel")
        if message.channel.id != counting_channel:
            return

        try:
            current_number = int(message.content.strip())
        except ValueError:
            await message.delete()
            return
        
        start_number = self.counting_data[server_id].get("start_number", 1)

        # Check if the current number matches the expected number
        if current_number != start_number:
            await message.delete()
            return

        # Check if the user is the same as the last user who sent a valid number
        last_user = self.counting_data[server_id].get("last_user")
        if last_user == str(message.author.id):
            await message.delete()
            await message.channel.send(f"{message.author.mention}, you need to wait for another user to send a number first.")
            return
        
        # Update the tracking for the next number and the user who sent it
        self.counting_data[server_id]["start_number"] = current_number + 1
        self.counting_data[server_id]["last_user"] = str(message.author.id)  # Store the user who sent the last valid number
        self.save_counting_data()

        await message.add_reaction("✅")

    @commands.command()
    async def setcountingchannel(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            await ctx.send("Please specify a channel.")
            return
        
        server_id = str(ctx.guild.id)
        if server_id not in self.counting_data:
            self.counting_data[server_id] = {}  # Add the server's data if it doesn't exist

        self.counting_data[server_id]["counting_channel"] = channel.id
        self.counting_data[server_id]["start_number"] = 1  # Reset the counting to start from 1

        self.save_counting_data()

        embed = discord.Embed(
            title="",
            description=f"**Counting channel set:** You can start counting from `{self.counting_data[server_id]['start_number']}`.\n\n- Text will be deleted when sent, the bot only allows numbers in the sequence.\n- If the number has a checkmark, it means the number has been accepted.",
            color=discord.Color.brand_green()
        )
        await channel.send(embed=embed)
        await ctx.send(f"Counting channel set to {channel.mention}.")

    @commands.command()
    async def setstartnumber(self, ctx, number: int):
        server_id = str(ctx.guild.id)
        if server_id not in self.counting_data:
            await ctx.send("The counting channel has not been set yet.")
            return
        
        self.counting_data[server_id]["start_number"] = number
        self.save_counting_data()

        embed = discord.Embed(
            title="",
            description=f"**Number set:** The counting will now start from `{self.counting_data[server_id]['start_number']}`.",
            color=discord.Color.brand_green()
        )
        await ctx.send(embed=embed)

    @app_commands.command(name="setcountingchannel", description="Set the counting channel for the server.")
    async def setcountingchannel_slash(self, interaction: discord.Interaction, channel: discord.TextChannel):
        server_id = str(interaction.guild.id)
        if server_id not in self.counting_data:
            self.counting_data[server_id] = {}

        self.counting_data[server_id]["counting_channel"] = channel.id
        self.counting_data[server_id]["start_number"] = 1  # Reset the counting to start from 1

        self.save_counting_data()

        embed = discord.Embed(
            title="",
            description=f"**Counting channel set:** You can start counting from `{self.counting_data[server_id]['start_number']}`.\n\n- Text will be deleted when sent, the bot only allows numbers in the sequence.\n- If the number has a checkmark, it means the number has been accepted.",
            color=discord.Color.brand_green()
        )
        await channel.send(embed=embed)
        await interaction.response.send_message(f"Counting channel set to {channel.mention}.", ephemeral=True)

    @app_commands.command(name="setstartnumber", description="Set the number to start counting from.")
    async def setstartnumber_slash(self, interaction: discord.Interaction, number: int):
        server_id = str(interaction.guild.id)
        if server_id not in self.counting_data:
            await interaction.response.send_message("The counting channel has not been set yet.", ephemeral=True)
            return
        
        self.counting_data[server_id]["start_number"] = number
        self.save_counting_data()

        embed = discord.Embed(
            title="",
            description=f"**Number set:** The counting will now start from `{self.counting_data[server_id]['start_number']}`.",
            color=discord.Color.brand_green()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Counting(bot))

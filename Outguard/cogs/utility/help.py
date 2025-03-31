import discord
from discord.ext import commands

class HelpDropdown(discord.ui.Select):
    def __init__(self, bot, original_embed):
        self.bot = bot
        self.original_embed = original_embed
        options = [
            discord.SelectOption(label="Fun", description="View fun commands."),
            discord.SelectOption(label="Security", description="View security commands."),
            discord.SelectOption(label="Utility", description="View utility commands."),
            discord.SelectOption(label="Moderation", description="View moderation commands."),
            discord.SelectOption(label="Developer", description="View developer only commands."),
        ]
        super().__init__(
            placeholder="Select a category...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Help", description="An unexpected error occurred.", colour=discord.Color.brand_red())
        
        # -> Handle dropdown options
        if self.values[0] == "Moderation":
            embed = discord.Embed(
                title="Moderation Commands",
                description="The commands shown below can only be used by moderators of the server.",
            )
            embed.add_field(name="`ban`", value="Bans a user from the current guild. `$ban [ID, @UserMention]`", inline=False)
            embed.add_field(name="`forceban`", value="Bans a user from the guild without them being within the server. `$forceban`", inline=False)
            embed.add_field(name="`kick`", value="Kicks a user from the current guild. `$ban [ID, @UserMention]`", inline=False)
            embed.add_field(name="`clear`", value="**Dangerous:** Deletes a bulk of messages at once. `$clear [Amount]`", inline=False)

        elif self.values[0] == "Fun":
            embed = discord.Embed(
                title="Fun Commands",
                description="Commands to have fun with the bot."
            )
            embed.add_field(name="`gru`", value="Gru gifs sent straight to the channel.", inline=False)

        elif self.values[0] == "Security":
            embed = discord.Embed(
                title="Security Commands",
                description="Commands to help secure the server from potential threats.",
            )
            embed.add_field(name="`lockdown`", value="Lockdown an individual channel. `$lockdown [channel] [messsage]`", inline=False)
            embed.add_field(name="`unlock`", value="Unlock an individual channel. `$lockdown [channel] [messsage]`", inline=False)
            embed.add_field(name="`lockdownall`", value="**Dangerous:** Lockdown all server channels. `$lockdownall`", inline=False)
            embed.add_field(name="`unlockall`", value="**Dangerous:** Unlocks all server channels. `$unlockall`", inline=False)
            embed.add_field(name="`slowmode`", value="Enforces a timer between messages sent.  `$slowmode [channel] [seconds]`", inline=False)

        elif self.values[0] == "Utility":
            embed = discord.Embed(
                title="Utility Commands",
                description="Commands to assist the user with information about the bot.",
            )
            embed.add_field(name="`ping`", value="Shows the bot's current latency when requested.", inline=False)
            embed.add_field(name="`invite`", value="Gives the recipitent user the bot & support server invite.", inline=False)
            embed.add_field(name="`help`", value="Gives you an interactive menu to explore features of our bot.", inline=False)
            embed.add_field(name="`servercount`", value="Shows the total number of servers the bot is in.", inline=False)
            embed.add_field(name="`autorole`", value="Brings up the sub-commands list to function this command.`", inline=False)

        elif self.values[0] == "Developer":
            embed = discord.Embed(
                title="Developer Commands",
                description="These commands are used to help assist the Sentinal developers.",
            )
            embed.add_field(name="`say`", value="Bot outputs messsage requested. `$say [message]`", inline=False)

        # -> Update the view to include the Back button
        view = HelpView(self.bot, self.original_embed, show_back=True)
        await interaction.response.edit_message(embed=embed, view=view)


class BackButton(discord.ui.Button):
    def __init__(self, bot, original_embed):
        super().__init__(label="Back", style=discord.ButtonStyle.gray)
        self.bot = bot
        self.original_embed = original_embed

    async def callback(self, interaction: discord.Interaction):
        # -> Reset to the original embed
        view = HelpView(self.bot, self.original_embed, show_back=False)
        await interaction.response.edit_message(embed=self.original_embed, view=view)


class HelpView(discord.ui.View):
    def __init__(self, bot, original_embed, show_back: bool = False):
        super().__init__()
        self.add_item(HelpDropdown(bot, original_embed))
        if show_back:
            self.add_item(BackButton(bot, original_embed))


class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["h"])
    async def help_command(self, ctx):
        original_embed = discord.Embed(
            title="Help Command",
            description=(
                "Use the dropdown menu below to select a category and view related commands. "
                "Each category contains commands grouped by functionality.\n\n"
                "Examples:\n"
                "`/help Fun` - Shows fun commands.\n"
                "`/help Utility` - Shows utility commands.\n"
                "`/help Security` - Shows secuirity commands.\n"
                "`/help Moderation` - Shows moderation commands.\n"
                "`/help Developer` - Shows developer only commands.\n"
            ),
        )
        original_embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        # -> Line 84: Removing the 'Back Button' from showing on the original embed.
        view = HelpView(self.bot, original_embed, show_back=False)
        await ctx.send(embed=original_embed, view=view)

    @discord.app_commands.command(name="help", description="Get help with bot commands")
    async def slash_help(self, interaction: discord.Interaction):
        original_embed = discord.Embed(
            title="Help Command",
            description=(
                "Use the dropdown menu below to select a category and view related commands. "
                "Each category contains commands grouped by functionality.\n\n"
                "Examples:\n"
                "`/help Fun` - Shows fun commands.\n"
                "`/help Utility` - Shows utility commands.\n"
                "`/help Security` - Shows secuirity commands.\n"
                "`/help Moderation` - Shows moderation commands.\n"
                "`/help Developer` - Shows developer only commands.\n"
            ),
        )
        original_embed.set_footer(text=f"Requested by {interaction.user}", icon_url=interaction.user.avatar.url)
        view = HelpView(self.bot, original_embed, show_back=False)
        await interaction.response.send_message(embed=original_embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))

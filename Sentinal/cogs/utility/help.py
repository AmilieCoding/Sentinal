import discord
from discord.ext import commands

class HelpDropdown(discord.ui.Select):
    def __init__(self, bot, original_embed):
        self.bot = bot
        self.original_embed = original_embed
        options = [
            discord.SelectOption(label="Moderation", description="View moderation commands."),
            discord.SelectOption(label="Utility", description="View utility commands."),
        ]
        super().__init__(
            placeholder="Select a category...",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Help", description="An unexpected error occurred.", colour=discord.Color.red())
        
        # Handle dropdown options
        if self.values[0] == "Moderation":
            embed = discord.Embed(
                title="Moderation Commands",
                description="The commands shown below can only be used by moderators of the server.",
                colour=discord.Colour.brand_green()
            )
            embed.add_field(name="`ban`", value="Bans a user from the current guild. `ID` `@UserMention`", inline=False)
            embed.add_field(name="`kick`", value="Kicks a user from the current guild. `ID` `@UserMention`.", inline=False)
        elif self.values[0] == "Utility":
            embed = discord.Embed(
                title="Utility Commands",
                description="Commands to assist the user with information about the bot.",
                colour=discord.Colour.brand_green()
            )
            embed.add_field(name="`ping`", value="Shows the bot's latency.", inline=False)

        # Update the view to include the Back button
        view = HelpView(self.bot, self.original_embed, show_back=True)
        await interaction.response.edit_message(embed=embed, view=view)


class BackButton(discord.ui.Button):
    def __init__(self, bot, original_embed):
        super().__init__(label="Back", style=discord.ButtonStyle.blurple)
        self.bot = bot
        self.original_embed = original_embed

    async def callback(self, interaction: discord.Interaction):
        # Reset to the original embed
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

    @commands.command(name="help")
    async def help_command(self, ctx):
        """Sends an embed explaining how to use the help command."""
        original_embed = discord.Embed(
            title="Help Command",
            description=(
                "Use the dropdown menu below to select a category and view related commands. "
                "Each category contains commands grouped by functionality.\n\n"
                "Examples:\n"
                "`/help Moderation` - Shows moderation commands.\n"
                "`/help Utility` - Shows utility commands."
            ),
            colour=discord.Colour.brand_green()
        )
        original_embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        view = HelpView(self.bot, original_embed, show_back=False)  # No Back button on the original embed
        await ctx.send(embed=original_embed, view=view)


async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCog(bot))

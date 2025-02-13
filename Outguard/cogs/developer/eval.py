import discord
from discord.ext import commands
import ast

class EvalCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def eval(self, ctx, *, code: str):
        """Evaluates Python code. (Prefix command)"""
        if ctx.author.id != 797474086820904971:  # Optional: restrict to specific user
            return await ctx.send("You are not authorized to use this command.")
        
        # Prepare the code for execution (safely)
        code = code.strip('` ')
        try:
            # Use a safer eval function (for example, using `ast.literal_eval` or `exec`)
            result = eval(code)  # You can replace this with a safer alternative if needed.
            await ctx.send(f"Result: {result}")
        except Exception as e:
            await ctx.send(f"Error: {e}")

    @discord.app_commands.command(name="eval", description="Evaluates Python code. (Slash command)")
    async def eval_slash(self, interaction: discord.Interaction, code: str):
        """Evaluates Python code. (Slash command)"""
        if interaction.user.id != 797474086820904971:  # Optional: restrict to specific user
            return await interaction.response.send_message("You are not authorized to use this command.")

        # Prepare the code for execution (safely)
        code = code.strip('` ')
        try:
            result = eval(code)  # You can replace this with a safer alternative if needed.
            await interaction.response.send_message(f"Result: {result}")
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}")

async def setup(bot):
    await bot.add_cog(EvalCog(bot))

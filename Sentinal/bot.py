import discord
from discord.ext import commands
import json
import os

# -> All intents and prefix command.
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix=">", intents=intents, help_command=None)

# -> Asynchronous function to load cogs from JSON
async def laad_cogs_van_json(json_file):
    with open(os.path.join(os.path.dirname(__file__), json_file), "r") as file:
        data = json.load(file)
        for cog in data["cogs"]:
            await bot.load_extension(cog)  # Await load_extension because it is asynchronous


# -> Loads all cogs in the 'cogs' folder!
async def load_extensions():
    try:
        await laad_cogs_van_json("cogs.json")
        print("Successfully loaded cogs.")
    except Exception as e:
        print(f"One or more cogs failed to load: {e}")


# -> Registers when the bot is online.
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd)
    try:
        await bot.tree.sync()  # Sync slash commands globally
        print("Slash commands have been synced.")
    except Exception as e:
        print(f"Failed to sync slash commands: {e}")

    print(f"Bot is online as user: {bot.user}")


# -> Main entry point to load extensions and start the bot.
async def main():
    await load_extensions()  # Load all cogs
    async with bot:
        await bot.start("LOL no")


# -> Run the bot.
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())

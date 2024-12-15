import discord
from discord.ext import commands

# -> All intents and prefix command.
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="$", intents=intents, help_command=None)


# -> Loads all cogs in the 'cogs' folder!
async def load_extensions():
    try:
        await bot.load_extension('cogs.utility.ping')
        await bot.load_extension('cogs.utility.help')
        await bot.load_extension('cogs.mod.kick')
        await bot.load_extension('cogs.mod.ban')
        await bot.load_extension('cogs.mod.unban')
        await bot.load_extension('cogs.mod.clear')
        await bot.load_extension('cogs.mod.lockdown')
        await bot.load_extension('cogs.mod.forceban')
        await bot.load_extension('cogs.mod.warn')
        await bot.load_extension('cogs.mod.slowmode')
        await bot.load_extension('cogs.developer.say')
        print("Successfully loaded cogs.")
    except Exception as e:
        print(f"One or more cogs failed to load: {e}")


# -> Registers when the bot is online.
@bot.event
async def on_ready():
    print(f"Bot is online as user: {bot.user}")

# -> Main entry point to load extensions and start the bot.
async def main():
    await load_extensions()  # Load all cogs
    async with bot:
        await bot.start("REMOVED FOR SECURITY")

# -> Run the bot.
if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
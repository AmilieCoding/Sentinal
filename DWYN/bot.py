import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio

# Temporary Solution until we figure out intents properly :sweat:
# Initialising command prefix and the bot's intents.
client = commands.Bot(command_prefix=">", intents=discord.Intents.all())

# Ensuring client has successfully logged in.
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# ---------------------------------------------------------------------------------------------------------
# IMPORTANT SECURITY WARNING - DO NOT IGNORE - FAILURE TO COMPLY RESULTS IN CONSEQUENCES - READ FULLY.
# Token Initialisation. Uses the token in your .env. Under NO circumstances should you EVER put your token
# as a hardcoded item in here. If you do and are caught your access to the support Discord will be revoked.
# YOU WERE WARNED.
# ---------------------------------------------------------------------------------------------------------
async def main():

    # Specify your cogs here!
    try:
        await client.load_extension('cogs.utility.ping')
        print(f"Successfully loaded all cogs.")
    except Exception as e:
        print(f"One or more cogs failed loading.")

    # Loads bot token.
    load_dotenv()
    bottoken = os.getenv("BOTTOKEN")
    if not bottoken:
        raise ValueError("Bot token is not set. Check your .env file or environment variables.")

    # Bot finally is run! Yippee!
    try:
        await client.start(bottoken)
    except KeyboardInterrupt:
        print("Shutting down gracefully...")
    finally:
        print("Bot has been shut down.")

# Bots entry point.
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("Forcefully stopped.")
import discord
import os
from dotenv import load_dotenv

# Prepares intents for usage, please review your bot dashboard if you are hosting your own service.
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

client = discord.Client(intents=intents)

# Ensuring client has successfully logged in.
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# Basic Calling System. Checks for prefix and directs the user to use a command.
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith('$'):
        await message.channel.send('Enter Desired Command')

# ---------------------------------------------------------------------------------------------------------
# IMPORTANT SECURITY WARNING - DO NOT IGNORE - FAILURE TO COMPLY RESULTS IN CONSEQUENCES - READ FULLY.
# Token Initialisation. Uses the token in your .env. Under NO circumstances should you EVER put your token
# as a hardcoded item in here. If you do and are caught your access to the support Discord will be revoked.
# YOU WERE WARNED.
# ---------------------------------------------------------------------------------------------------------
load_dotenv()
client.run(os.getenv("BOTTOKEN"))
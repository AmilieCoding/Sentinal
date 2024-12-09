import discord
import os
from dotenv import load_dotenv

# ---------------------------------------------------------------------------------------------------------
# IMPORTANT SECURITY WARNING - DO NOT IGNORE - FAILURE TO COMPLY RESULTS IN CONSEQUENCES - READ FULLY.
# Token Initialisation. Uses the token in your .env. Under NO circumstances should you EVER put your token
# as a hardcoded item in here. If you do and are caught your access to the support Discord will be revoked.
# YOU WERE WARNED.
# ---------------------------------------------------------------------------------------------------------
load_dotenv()
print(os.getenv("BOTTOKEN"))
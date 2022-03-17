# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2021-2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

# The libraries that are for the bot.
import asyncio
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

# Coloured text from logger file and Prefix from database file.
from utils import logger, database

# Load the bot token. You should create a file named .env and write the token.
# Example: TOKEN='(your token)'
load_dotenv()
token = os.getenv('TOKEN')

# Create the activity for Discord. Idle looks cool.
activity = discord.Activity(type=discord.ActivityType.watching,
                            name=f'24/7', status=discord.Status.idle)

# Selects all intents and prefix, case-insensitive, description.
bot = commands.Bot(command_prefix=database.get_prefix,
                   case_insensitive=True,
                   description="EnSave is a Discord bot, that adds some cool utility commands and some music commands. "
                               "Have fun and explore the commands of EnSave.",
                   activity=activity,
                   status=discord.Status.idle,
                   intents=discord.Intents.all())


# Load all the cogs, then print the cog names that have been loaded.
async def load_cogs():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            loader = filename[:-3]
            await bot.load_extension(f'cogs.{loader}')
            logger.print_color(f'{loader.capitalize()} has been loaded', 'HEADER')
asyncio.run(load_cogs())


# Run the bot with token (.env file)
async def main():
    async with bot:
        await bot.start(token, reconnect=True)

if __name__ == "__main__":
    asyncio.run(main())

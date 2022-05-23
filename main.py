# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it
#
# (C) 2021-2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

# This first file is mostly documented but the others aren't.
# If you want to help me add comments then open a PR on GitHub

import asyncio
import os

import colorama
import discord
from colorama import Fore
from discord.ext import commands, ipc
from dotenv import load_dotenv

from utils import database

# Auto reset settings in colorama
colorama.init(autoreset=True)

# Load the bot token. You should create a file named .env and write the token.
# Example: TOKEN='(your token)'
load_dotenv()
token = os.getenv('TOKEN')


class Main(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ipc = ipc.Server(self, secret_key=os.getenv('SECRET_KEY'))


# Create the activity for idle
activity = discord.Activity(type=discord.ActivityType.watching,
                            name=f'24/7', status=discord.Status.idle)

# Create the bot
bot = Main(command_prefix=database.get_prefix,
           case_insensitive=True,
           description="EnSave offers you moderation, fun and utility commands. "
                       "We have frequent updates and fix bugs almost instantly. "
                       "This includes everything you need from a discord bot.",
           activity=activity,
           status=discord.Status.idle,
           intents=discord.Intents.all())


# Load all the cogs, then print the cog names that have been loaded
# Also run the bot with token from .env file
async def main():
    await bot.ipc.start()

    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('_'):
            loader = filename[:-3]
            await bot.load_extension(f'cogs.{loader}')
            print(f'{Fore.LIGHTMAGENTA_EX}{loader.capitalize()} has been loaded')

    async with bot:
        await bot.start(token, reconnect=True)


if __name__ == "__main__":
    asyncio.run(main())

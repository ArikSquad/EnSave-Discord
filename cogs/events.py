# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import datetime
import json
import os

from discord.ext import commands
from dotenv import load_dotenv

from utils import logger

load_dotenv()
danbot = os.getenv('DBHAPI')


class Events(commands.Cog, description="Add the events to the bot"):
    def __init__(self, bot):
        self.bot = bot

    # This will be run, after the bot is ready.
    @commands.Cog.listener()
    async def on_ready(self):
        # Send information to DanBot.
        # DanBotClient(bot, key=danbot, autopost=True)
        # Print some information about the bot.
        print("Logging in... at the time of " + str(datetime.datetime.now()))
        print(f'{logger.WARNING}{self.bot.user} has connected to Discord!{logger.END}')
        print(f"Name: {logger.CYAN}{self.bot.user.name}{logger.END}")
        print(f"ID: {logger.CYAN}{self.bot.user.id}{logger.END}")
        print(f'{logger.BOLD}###########################################{logger.END}')
        print(f"Connected to {logger.GREEN}{len(self.bot.guilds)} guilds{logger.END}")

        with open("db/users.json", "r") as f:
            data = json.load(f)
        guild = self.bot.get_guild(770634445370687519)
        async for member in guild.fetch_members():
            if str(member.id) not in data and not member.bot:
                data[str(member.id)] = {}
                data[str(member.id)]["experience"] = 0
                data[str(member.id)]["level"] = 0
                data[str(member.id)]["sent"] = 1
        with open("db/users.json", 'w') as f:
            json.dump(data, f, indent=4)

    # This even will be run after the bot leaves a guild.
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        # This command just removed the prefix from the database.
        with open('db/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes.pop(str(guild.id))
        with open('db/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

    # This event will be run after bot joins a guild.
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        # Opens the prefixes.json to read the prefixes.
        with open('db/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        # This is the default prefix. You can change it if you want to!
        prefixes[str(guild.id)] = '.'
        # Opens the prefixes.json to write the prefixes.
        with open('db/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)


async def setup(bot):
    await bot.add_cog(Events(bot))

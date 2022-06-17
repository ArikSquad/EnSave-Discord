# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import datetime

from colorama import Fore
from discord.ext import commands

from utils import db


class Events(commands.Cog, description="Events"):
    EMOJI = "📅"

    def __init__(self, bot):
        self.bot = bot

    # When the bot is ready, send information about the bot
    @commands.Cog.listener()
    async def on_ready(self):
        print("Logging in... at the time of " + str(datetime.datetime.now()))
        print(f'{Fore.LIGHTRED_EX}{self.bot.user} has connected to Discord!')
        print(f"Name: {Fore.LIGHTCYAN_EX}{self.bot.user.name}")
        print(f"ID: {Fore.LIGHTCYAN_EX}{self.bot.user.id}")
        print(f'{Fore.LIGHTWHITE_EX}###########################################')
        print(f"Currently in {Fore.LIGHTGREEN_EX}{len(self.bot.guilds)} guilds")

    # When the bot is removed from a guild, remove it from the database
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        db.remove_guild(guild.id)

    # When the bot joins a guild, it creates it in the database
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        self.bot.update_db()

    # When a member joins, it adds it to the database
    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.bot.update_db()


async def setup(bot):
    await bot.add_cog(Events(bot))

# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import datetime
import json

from colorama import Fore
from discord.ext import commands


class Events(commands.Cog, description="Events"):
    EMOJI = "📅"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logging in... at the time of " + str(datetime.datetime.now()))
        print(f'{Fore.LIGHTRED_EX}{self.bot.user} has connected to Discord!')
        print(f"Name: {Fore.LIGHTCYAN_EX}{self.bot.user.name}")
        print(f"ID: {Fore.LIGHTCYAN_EX}{self.bot.user.id}")
        print(f'{Fore.LIGHTWHITE_EX}###########################################')
        print(f"Currently in {Fore.LIGHTGREEN_EX}{len(self.bot.guilds)} guilds")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        with open('db/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        with open('db/guilds.json', 'r') as f2:
            guilds = json.load(f2)

        prefixes.pop(str(guild.id))
        guilds.pop(str(guild.id))

        with open('db/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        with open('db/guilds.json', 'w') as f2:
            json.dump(guilds, f2, indent=4)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with open('db/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        with open('db/guilds.json', 'r') as f2:
            guilds = json.load(f2)

        prefixes[str(guild.id)] = '.'
        guilds[str(guild.id)] = {
            "spy_edit": False,
            "spy_delete": False,
            "spy_channel": None
        }
        with open('db/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        with open('db/guilds.json', 'w') as f2:
            json.dump(guilds, f2, indent=4)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('db/users.json', 'r') as f:
            users = json.load(f)

        if member.bot:
            return

        if member.id not in users:
            users[str(member.id)] = {
                "premium": False,
                "messages": 0
            }

            with open('db/users.json', 'w') as f:
                json.dump(users, f, indent=4)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        with open('db/codes.json', 'r') as f:
            codes = json.load(f)

        amount = 0
        for _ in codes["codes"]:
            amount = amount + 1

        found = False
        number = 0
        for i in range(amount):
            if codes["codes"][str(i)][1] == int(message.id):
                found = True
                number = i

        if found:
            codes["codes"][number][1] = None
            with open('db/codes.json', 'w') as f:
                json.dump(codes, f, indent=4)


async def setup(bot):
    await bot.add_cog(Events(bot))

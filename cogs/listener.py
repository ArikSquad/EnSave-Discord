# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2021-2022 MikArt
# Released under the Apache License 2.0
#
# -----------------------------------------------------------
import datetime

import discord
from colorama import Fore
from discord.ext import commands

from utils import db, utility


class Events(commands.Cog, description="Events"):
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
        db.set_guild_spy_channel(guild.id, self.bot.get_guild(guild.id).system_channel.id)

    # When a member joins, it adds it to the database
    # noinspection PyUnusedLocal
    @commands.Cog.listener()
    async def on_member_join(self, member):
        self.bot.update_db()

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        all_commands = ["admin", "dashboard", "help", "mcserver", "bedwars", "skin", "redeem", "spy", "role", "play",
                        "stop", "pause", "skip", "disconnect", "spy", "volume", "shuffle", "playing", "resume", "lock",
                        "unlock", "clear", "redeem"]
        if message.author.bot:
            return
        if not message.guild:
            return
        if message.content.startswith(utility.get_prefix_id(message.guild.id)):
            after_check = (message.content.split(utility.get_prefix_id(message.guild.id))[1]).split(' ')[0]
            if after_check in all_commands:
                embed = discord.Embed(title='Slash Commands',
                                      description='As you probably have seen, Discord is changing to use more of the '
                                                  'slash commands, So are we! The old commands '
                                                  'are no longer supported.',
                                      color=discord.Color.from_rgb(48, 50, 54))
                embed.add_field(name='How to use these?',
                                value="It's easy! You only need to type `/` before the command!")
                await message.channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Events(bot))

# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2021-2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

# The libraries that are for the bot.
import datetime
import json
import os

import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands

# Coloured text from logger file and Prefix from database file.
from utils import logger, database

# To change the token create a file named .env and write the token.
# Example usage: TOKEN='(your token)'
load_dotenv()
token = os.getenv('token')


# Create the activity for Discord. Idle looks cool.
activity = nextcord.Activity(type=nextcord.ActivityType.watching,
                             name=f'24/7', status=nextcord.Status.idle)

# Selects all intents and prefix, case-insensitive, description.
bot = commands.Bot(command_prefix=database.get_prefix,
                   case_insensitive=True,
                   description="Utilities Bot.",
                   activity=activity,
                   status=nextcord.Status.idle,
                   intents=nextcord.Intents.all())


# This event will be run after bot joins a guild.
@bot.event
async def on_guild_join(guild):
    # Opens the prefixes.json to read the prefixes.
    with open('db/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    # This is the default prefix. You can change it if you want to!
    prefixes[str(guild.id)] = '.'
    # Opens the prefixes.json to write the prefixes.
    with open('db/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


# This even will be run after the bot leaves a guild.
@bot.event
async def on_guild_remove(guild):
    # This command just removed the prefix from the database.
    with open('db/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('db/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


# This is a command to change the prefix.
@bot.command(name="prefix", help="Change the prefix of the guild.",
             aliases=["changeprefix"])
@commands.has_permissions(administrator=True)
async def change_prefix(ctx, prefix):
    embed = nextcord.Embed(title="Moderation",
                           description=f"Changed the prefix to: " + prefix,
                           color=nextcord.Color.gold())
    await ctx.send(embed=embed)

    # Opens the prefixes.json to read the prefixes.
    with open('db/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix

    # Writes the prefixes back to the file
    with open('db/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    print(f'Changed prefix in {ctx.guild} to {prefix}. Command was ran user {ctx.message.author}.')


# This will be run, after the bot is ready.
@bot.event
async def on_ready():
    # Print some information about the bot.
    print("Logging in... at the time of " + str(datetime.datetime.now()))
    print(f'{logger.WARNING}{bot.user} has connected to Discord!{logger.END}')
    print(f"Name: {logger.CYAN}{bot.user.name}{logger.END}")
    print(f"ID: {logger.CYAN}{bot.user.id}{logger.END}")
    print(f'{logger.BOLD}###########################################{logger.END}')
    print(f"Connected to {logger.GREEN}{len(bot.guilds)} guilds{logger.END}")

    with open("db/users.json", "r") as f:
        data = json.load(f)
    guild = bot.get_guild(770634445370687519)
    async for member in guild.fetch_members():
        if str(member.id) not in data and not member.bot:
            data[str(member.id)] = {}
            data[str(member.id)]["experience"] = 0
            data[str(member.id)]["level"] = 0
            data[str(member.id)]["sent"] = 1
    with open("db/users.json", 'w') as f:
        json.dump(data, f, indent=4)


# Load all the cogs, then tell what have been loaded.
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        loader = filename[:-3]
        bot.load_extension(f'cogs.{loader}')
        print(f'{logger.HEADER}{loader.capitalize()} has been loaded{logger.END}')

# Run the bot with token (.env file)
if __name__ == "__main__":
    bot.run(token, reconnect=True)

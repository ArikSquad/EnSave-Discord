# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import datetime
import json
import logging
import os

import nextcord
from dotenv import load_dotenv
from nextcord.ext import commands

# Save logs to file with only hours, minutes and seconds
from utils import logger

# Logging with max 100 lines
logging.basicConfig(filename=f'logs/latest.log')

# To change the token create a file named .env and write the token.
# Example usage: TOKEN='(your token)'
load_dotenv()
token = os.getenv('token')


# Gets prefix in db/prefixes.json. PyUnusedLocal for the ctx warning.
# noinspection PyUnusedLocal
def get_prefix(ctx, message):
    try:
        with open('db/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes[str(message.guild.id)]
    except KeyError:
        with open('db/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(message.guild.id)] = '.'

        with open('db/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)


# Create the activity for Discord. Idle looks cool
activity = nextcord.Activity(type=nextcord.ActivityType.watching,
                             name=f'fast updates', status=nextcord.Status.idle)

# Selects all intents and prefix, case-insensitive, description.
bot = commands.Bot(command_prefix=get_prefix,
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

    prefixes[str(guild.id)] = '.'
    # Opens the prefixes.json to write the prefixes.
    with open('db/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


# This even will be run after the bot leaves a guild.
@bot.event
async def on_guild_remove(guild):
    with open('db/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('db/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


# Sends a message that these commands only support slash commands.
@bot.command(name='oldsupport',
             aliases=['rockpaperscrissors', 'rps', "rollingdice", "diceroll",
                      "rolldice", 'dice', "8Ball", '8ba', 'eightball', 'slot', 'bet',
                      'slots', 'cookie', 'coinflip', 'doggo', 'dog'],
             description="Removed commands.", hidden=True)
async def old_dated(ctx):
    embed = nextcord.Embed(title=f"Slash Commands.", description=f"{ctx.command} is no longer "
                                                                 f"supported without slash command.",
                           color=ctx.author.color)
    await ctx.reply(embed=embed)


# A command to change the prefix
@bot.command(name="prefix", description="Change the prefix.", aliases=["changeprefix"])
@commands.has_permissions(administrator=True)
async def _change_prefix(ctx, prefix):
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
    # Print the information about the bot.
    print("Logging in... at the time of " + str(datetime.datetime.now()))
    print(f'{logger.ColoredText.WARNING}{bot.user} has connected to Discord!{logger.ColoredText.END}')
    print(f"Name: {logger.ColoredText.CYAN}{bot.user.name}{logger.ColoredText.END}")
    print(f"ID: {logger.ColoredText.CYAN}{bot.user.id}{logger.ColoredText.END}")
    print(f'{logger.ColoredText.BOLD}####################################{logger.ColoredText.END}')
    print(f"Connected to {logger.ColoredText.GREEN}{len(bot.guilds)} guilds{logger.ColoredText.END}")


# Load all the cogs.
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        loader = filename[:-3]
        bot.load_extension(f'cogs.{loader}')
        print(f'{logger.ColoredText.HEADER}{loader.capitalize()} has been loaded{logger.ColoredText.END}')

# Run the bot with token (.env file)
if __name__ == "__main__":
    bot.run(token, reconnect=True)

# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2021 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import json
import logging
import os

import discord
from discord.ext import commands
from discord_components import DiscordComponents
from discord_slash import SlashCommand as SlashComma
from dotenv import load_dotenv
from pretty_help import DefaultMenu, PrettyHelp

# Save logs to file with only hours, minutes and seconds
logging.basicConfig(filename=f'logs/latest.log'),

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


# The activity variable
activity = discord.Activity(type=discord.ActivityType.watching,
                            name=f'fast updates', status=discord.Status.idle)

# Selects all intents and prefix, case-insensitive, description.
bot = commands.Bot(command_prefix=get_prefix,
                   case_insensitive=True,
                   description="Utilities Bot.",
                   activity=activity,
                   status=discord.Status.idle,
                   intents=discord.Intents.all())


# The variable for slash commands.
slash = SlashComma(bot, sync_commands=True)

# Variable for the help menus
menu = DefaultMenu('◀️', '▶️', '❌', active_time=5, delete_after_timeout=True)

# Makes the help menu
bot.help_command = PrettyHelp(navigation=menu, color=discord.Colour.green(), no_category="Other")


# Ran when bot joins the server.
@bot.event
async def on_guild_join(guild):
    with open('db/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('db/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


# Ran when bot leaves server.
@bot.event
async def on_guild_remove(guild):
    with open('db/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('db/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


# Sends a message that these commands only support slash commands.
@bot.command(name='none',
             aliases=['ttt', 'rockpaperscrissors', 'rps', "rollingdice", "diceroll",
                      "rolldice", 'dice', "8Ball", '8ba', 'eightball', 'slot', 'bet',
                      'slots', 'tictactoe', 'invite', 'ping', 'latency', "supportserver",
                      "feedbackserver", "discord", 'server', 'github', 'sourcecode',
                      'cookie', 'password', 'hello', 'slap', 'say', 'tell', 'coinflip',
                      'av', 'doggo', 'dog'], hidden=True)
async def old_dated(ctx):
    embed = discord.Embed(title=f"Slash Commands.", description="We stopped supporting commands without slash. "
                                                                "Please use slash commands. But keep in mind that we "
                                                                "haven't made Music yet. So you can't use the music "
                                                                "commands yet with slash commands.",
                          color=ctx.author.color)
    await ctx.reply(embed=embed)


# Create command to change prefix
@bot.command(help="Change the prefix.", name="prefix")
@commands.has_permissions(administrator=True)
async def change_prefix(ctx, prefix):
    embed = discord.Embed(title="Moderation",
                          description=f"Changed the prefix to: " + prefix,
                          color=discord.Color.gold())
    await ctx.send(embed=embed)

    # Opens the prefixes.json to read the data in it
    with open('db/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix

    # writes prefixes in prefixes.json
    with open('db/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    print(f'Changed prefix in {ctx.guild} to {prefix}. Command was ran user {ctx.message.author}.')


# Class to choose a print color
class ColoredText:
    HEADER = '\033[95m'

    BLUE = '\033[94m'

    # My personal favourite
    CYAN = '\033[96m'

    GREEN = '\033[92m'

    WARNING = '\033[93m'

    FAIL = '\033[91m'

    END = '\033[0m'

    BOLD = '\033[1m'

    UNDERLINE = '\033[4m'


# This will be run, after the bot is ready.
@bot.event
async def on_ready():
    DiscordComponents(bot)

    # Print the information about the bot.
    print("Logging in...")
    print(f'{ColoredText.WARNING}{bot.user} has connected to Discord!{ColoredText.END}')
    print(f"Name: {ColoredText.CYAN}{bot.user.name}{ColoredText.END}")
    print(f"ID: {ColoredText.CYAN}{bot.user.id}{ColoredText.END}")
    print(f'{ColoredText.BOLD}####################################{ColoredText.END}')
    print(f"Connected to {ColoredText.GREEN}{len(bot.guilds)} guilds{ColoredText.END}")


# Load all the cogs.
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        loader = filename[:-3]
        bot.load_extension(f'cogs.{loader}')
        print(f'{ColoredText.HEADER}{loader.capitalize()} has been loaded{ColoredText.END}')

# Run the bot with token (.env file)
if __name__ == "__main__":
    bot.run(token, reconnect=True)
    # reconnect=True is for it to reconnect when lost connection.

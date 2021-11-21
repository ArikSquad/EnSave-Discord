import json
import logging
import os

import discord
from discord.ext import commands
from discord_components import DiscordComponents
from discord_slash import SlashCommand
from dotenv import load_dotenv
from pretty_help import DefaultMenu, PrettyHelp

logging.basicConfig(level=logging.WARNING)
load_dotenv()
token = os.getenv('token')


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


bot = commands.Bot(
    command_prefix=get_prefix, case_insensitive=True,
    description="This is a discord utility bot. Thanks for using this bot",
    intents=discord.Intents.all()
)
slash = SlashCommand(bot, sync_commands=True)

menu = DefaultMenu(
    '◀️', '▶️', '❌',
    active_time=5,
    delete_after_timeout=True,
)
bot.help_command = PrettyHelp(navigation=menu, color=discord.Colour.green(), no_category="Other", )


@bot.event
async def on_guild_join(guild):
    with open('db/prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('db/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open('db/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('db/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.command(name='none',
             aliases=['ttt', 'rockpaperscrissors', 'rps', "rollingdice", "diceroll",
                      "rolldice", 'dice', "8Ball", '8ba', 'eightball', 'slot', 'bet',
                      'slots', 'tictactoe', 'invite', 'ping', 'latency', "supportserver",
                      "feedbackserver", "discord", 'server', 'github', 'sourcecode',
                      'cookie', 'password', 'hello', 'slap', 'say', 'tell'])
async def nocommand(ctx):
    embed = discord.Embed(title=f"Slash Commands.", description="We stopped supporting game commands without slash."
                                                                " Please use slash commands.",
                          color=ctx.author.color())

    await ctx.send(embed=embed)


@bot.command(help="Change the prefix.", name="ChangePrefix")
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    prefixss = discord.Embed(title="Moderation",
                             description=f"Changed the prefix to: " + prefix,
                             color=discord.Color.gold())
    await ctx.send(embed=prefixss)
    with open('db/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('db/prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    print(f'Changed prefix in {ctx.guild} to {prefix}. Command was ran user {ctx.message.author}.')


class ColoredText:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


@bot.event
async def on_ready():
    DiscordComponents(bot)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                        name=f'{len(bot.guilds)} guilds'))

    print("Logging in...")
    print(f'{ColoredText.WARNING}{bot.user} has connected to Discord!{ColoredText.END}')
    print(f"Name: {ColoredText.CYAN}{bot.user.name}{ColoredText.END}")
    print(f"ID: {ColoredText.CYAN}{bot.user.id}{ColoredText.END}")
    print(f'{ColoredText.BOLD}####################################{ColoredText.END}')
    print(f"Connected to {ColoredText.GREEN}{len(bot.guilds)} guilds{ColoredText.END}")


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        loader = filename[:-3]
        bot.load_extension(f'cogs.{loader}')
        print(f'{ColoredText.HEADER}{loader.capitalize()} has been loaded{ColoredText.END}')

if __name__ == "__main__":
    bot.run(token, reconnect=True)

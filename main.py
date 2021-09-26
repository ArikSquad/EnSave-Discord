import asyncio
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


def get_prefix(ctx, message):
    try:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes[str(message.guild.id)]
    except KeyError:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(message.guild.id)] = '.'

        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)


bot = commands.Bot(command_prefix=get_prefix, case_insensitive=True)
slash = SlashCommand(bot, sync_commands=True)

menu = DefaultMenu(
    '◀️', '▶️', '❌',
    active_time=5,
    delete_after_timeout=True,
)
bot.help_command = PrettyHelp(navigation=menu, color=discord.Colour.green(), no_category="Other", )


@bot.event
async def on_member_join(member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = f'Welcome {member.mention} to {guild.name}!'
        await guild.system_channel.send(to_send)


@bot.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '.'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.command(help="Change the prefix.", name="ChangePrefix")
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    prefixss = discord.Embed(title="Moderation",
                             description=f"Changed the prefix to: " + prefix,
                             color=discord.Color.gold())
    await ctx.send(embed=prefixss)
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    print(f'Changed prefix in {ctx.guild}. Command was ran user {ctx.message.author}.')


async def status_task():
    while True:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Rick Astley"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="AriCC"))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching,
                                                            name=f'{len(bot.guilds)} guilds'))
        await asyncio.sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="Minecraft"))
        await asyncio.sleep(10)


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

    bot.loop.create_task(status_task())
    print(f"{ColoredText.CYAN}Started bot loop for custom RPC{ColoredText.END}")

    print("Logging in...")
    print(f'{ColoredText.WARNING}{bot.user} has connected to Discord!{ColoredText.END}')
    print(f'{ColoredText.BOLD}####################################{ColoredText.END}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        loader = filename[:-3]
        bot.load_extension(f'cogs.{loader}')
        print(f'{loader.capitalize()} has been loaded')

bot.run(token, reconnect=True)

import random

import discord
from discord.ext import commands
from discord_slash import SlashCommand
import json
import os
from dotenv import load_dotenv
from pretty_help import DefaultMenu, PrettyHelp
from discord_components import DiscordComponents

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


bot = commands.Bot(command_prefix=get_prefix)
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
                             description=f"Changed the prefix to ' + prefix",
                             color=discord.Color.gold())
    await ctx.message.delete()
    await ctx.send(embed=prefixss)
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    print(f'Changed prefix in {ctx.guild}. Command was ran user {ctx.message.author}.')


@bot.event
async def on_ready():
    DiscordComponents(bot)

    randomints = random.randint(1, 3)

    if randomints == 1:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you"))
    elif randomints == 2:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Rickroll"))
    elif randomints == 3:
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="AriCC"))

    print("Logging in...")
    print(f'{bot.user} has connected to Discord!')
    print(f'####################################')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run(token, reconnect=True)

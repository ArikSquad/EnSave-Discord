import datetime
import traceback
import discord
from discord.ext import commands
from discord_slash import SlashCommand
import json
import os


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


@bot.command(help="Change the prefix.", brief="Change the prefix.")
@commands.has_permissions(administrator=True)
async def changeprefix(ctx, prefix):
    prefixss = discord.Embed(title="Admin",
                             description=f"Changed the prefix to ' + prefix",
                             color=discord.Color.dark_red())

    await ctx.message.delete()
    await ctx.send(embed=prefixss)
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)




@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="you"))

    print("Logging in...")
    print("Bot can now be used.")
    print("EnSave is now on the use")
    print("----------------------")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run('ODEyODA4ODY1NzI4OTU0Mzk5.YDGJPg.LLZpCQsIf8zZR8Nb02S4ofoq-qI')

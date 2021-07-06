import discord
from discord.utils import get
from discord.ext import commands
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
import youtube_dl
import time
import json
import os
import aiohttp
import random
import urllib
import urllib.parse
import urllib.request
import asyncio
import re


def get_prefix(client, message):
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
slash = SlashCommand(bot, sync_commands=True, override_type=True)


@bot.command()
@commands.cooldown(1, 2, commands.BucketType.user)
async def slap(ctx, member: discord.User = None):
    emb = discord.Embed(title=None,
                        description=f"{ctx.message.author.mention} slaps {member.mention} in the face!",
                        color=0x3498db)

    await ctx.send(embed=emb)


@bot.command()
async def dog(ctx):
    await ctx.message.delete()
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://random.dog/woof.json") as r:
            data = await r.json()
            embed = discord.Embed(
                title="Doggo",
                color=ctx.author.color
            )
            embed.set_image(url=data['url'])

            await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def meme(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="", description="")

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])

            await ctx.send(embed=embed)


emojis2 = ['heart', 'verifycyan', 'uhh']


@bot.command()
async def noob(ctx, member: discord.Member):
    await ctx.message.delete()
    if member is not None:
        await ctx.send(f"{member.mention} is noob.")
        await member.send(f"{ctx.message.author} said you were bad!")
    else:
        await ctx.send("You forgot who!")


@bot.command()
async def react(ctx, reaction: str):
    await ctx.message.delete()
    try:
        message = await ctx.send("Reacting to this message...")
        await message.add_reaction(reaction)
    except Exception:
        for emoji in emojis2:
            message = await ctx.send("Reacting to this message...")
            await message.add_reaction(emoji)


@slash.slash(name="choice",
             description="Choice between two numbers.",
             guild_ids=[770634445370687519],
             options=[
               create_option(
                 name="option",
                 description="Doge or No Doge.",
                 option_type=3,
                 required=True,
                 choices=[
                  create_choice(
                    name="1",
                    value="DOGE!"
                  ),
                  create_choice(
                    name="2",
                    value="NO DOGE"
                  )
                ]
               )
             ])
async def test(ctx, option: str):
    await ctx.send(f"Wow, you actually chose {option}? :(")



@bot.command()
async def imgay(ctx):
    await ctx.message.delete()
    embed = discord.Embed(title="Your Gay?",
                          description=f"Yes, {ctx.message.author.mention} is gay.",
                          color=discord.Color.magenta())
    async with ctx.typing():
        await asyncio.sleep(1)
    await ctx.send(embed=embed)


@bot.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
async def play(ctx, *, search):
    await ctx.message.delete()
    start = discord.Embed(title="Music", description="Trying to find your song!", color=discord.Color.purple())
    start1 = await ctx.send(embed=start)

    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + urllib.parse.quote(search))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    url = "https://www.youtube.com/watch?v=" + video_ids[0]

    embed1 = discord.Embed(title="Music Link",
                           url=f'{url}',
                           description=f"Is this what you wanted to hear {ctx.message.author}?",
                           color=0xFF5733)
    await start1.edit(embed=embed1)

    embed2 = discord.Embed(title="Music",
                           description=f"Downloading the music for {ctx.message.author}!",
                           color=discord.Color.blue())

    embed3 = discord.Embed(title="Music",
                           description=f"Starting to play {ctx.message.author.mention}",
                           color=discord.Color.dark_red())

    permission = discord.Embed(title="Music",
                               description=f'Wait for the current playing music end or use the "leave" command.'
                                           f' {ctx.message.author.mention}',
                               color=discord.Color.red())

    stop = discord.Embed(title="Music",
                            description=f'Stopped playing the music! {ctx.message.author.mention}',
                            color=discord.Color.green())

    isnt = discord.Embed(title="Music",
                         description=f"{ctx.message.author.mention} isn't in a voice chat",
                         color=discord.Color.green())

    playing = discord.Embed(title="Music",
                            description=f'Currently playing the music!',
                            color=discord.Color.gold())

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send(embed=permission)
        return
    msg = await ctx.send(embed=embed2)
    print("SOMEONE WANTS MUSICCCCCC READDYYY?!!?!?!?!?")
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')
    await msg.edit(embed=embed3)
    voice_channel = ctx.author.voice.channel
    if voice_channel is not None:
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:/FFMPEG/ffmpeg.exe",
                                       source="D:/misc/EnSave Reborn/song.mp3"))
        while vc.is_playing():
            await msg.edit(embed=playing)
        await msg.edit(embed=stop)
    else:
        await ctx.send(embed=isnt)


@bot.event
async def on_member_join(self, member):
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


@bot.command(help="Multiply numbers.", brief="Multiply numbers.")
async def multiply(ctx, left: int, right: int):
    as4 = discord.Embed(title="Maths",
                        description=f"The answer is: {left * right}! {ctx.message.author.mention}",
                        color=discord.Color.dark_red())

    await ctx.message.delete()
    await ctx.send(embed=as4)


@bot.command(help="Multiply numbers.", brief="Multiply numbers.")
async def remove(ctx, left: int, right: int):
    remove = discord.Embed(title="Maths",
                          description=f"The answer is: {left - right}! {ctx.message.author.mention}",
                          color=discord.Color.dark_red())

    await ctx.message.delete()
    await ctx.send(embed=remove)


@bot.command(help="Divide numbers.", brief="Divide numbers.")
async def divide(ctx, left: int, right: int):
    divide = discord.Embed(title="Maths",
                               description=f"The answer is: {left / right}! {ctx.message.author.mention}",
                               color=discord.Color.dark_red())

    await ctx.message.delete()
    await ctx.send(embed=divide)


@bot.command(pass_context=True, brief="Makes the bot join your channel", aliases=['j', 'jo'])
async def join(ctx):
    await ctx.message.delete()
    channel = ctx.message.author.voice.channel

    no_connect = discord.Embed(title="Music",
                          description=f"You are not connected to a voice channel. {ctx.message.author.mention}",
                          color=discord.Color.dark_red())

    joined = discord.Embed(title="Music",
                              description=f"Joining {channel} to play the latest song by {ctx.message.author.mention}",
                              color=discord.Color.dark_red())
    plays = discord.Embed(title="Music",
                           description=f"Currently playing the latest song. {ctx.message.author.mention}",
                           color=discord.Color.green())
    stop = discord.Embed(title="Music",
                           description=f"Stopped playing the latest song. {ctx.message.author.mention}",
                           color=discord.Color.red())
    if not channel:
        await ctx.send(embed=no_connect)
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    msg = await ctx.send(embed=joined)

    voice.play(discord.FFmpegPCMAudio(executable="C:/FFMPEG/ffmpeg.exe", source="D:/misc/EnSave Reborn/song.mp3"))
    while voice.is_playing():
        await msg.edit(embed=plays)
    await msg.edit(embed=stop)

@bot.command()
async def pause(ctx):
    await ctx.message.delete()
    paused = discord.Embed(title="Music",
                               description=f"Paused by {ctx.message.author}!",
                               color=discord.Color.blue())

    error = discord.Embed(title="Music",
                           description=f"Currently no audio is playing. {ctx.message.author.mention}",
                           color=discord.Color.dark_red())


    voice = get(bot.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel
    if voice.is_playing():
        voice.pause()
        await ctx.send(embed=paused)
    else:
        await ctx.send(embed=error)

@bot.command()
async def resume(ctx):
    await ctx.message.delete()
    resumed = discord.Embed(title="Music",
                          description=f"Resuming the music by {ctx.message.author}!",
                          color=discord.Color.green())

    error = discord.Embed(title="Music",
                          description="The audio is not paused.",
                          color=discord.Color.dark_red())

    voice = get(bot.voice_clients, guild=ctx.guild)
    channel = ctx.message.author.voice.channel

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    if voice.is_paused():
        voice.resume()
        await ctx.send(embed=resumed)
    else:
        await ctx.send(embed=error)

@bot.command()
async def stop(ctx):
    await ctx.message.delete()
    stopped = discord.Embed(title="Music",
                            description=f"Stopped the music! Command ran by {ctx.message.author}",
                            color=discord.Color.gold())

    error = discord.Embed(title="Music",
                          description=f"Bot isn't connected. {ctx.message.author.mention}",
                          color=discord.Color.dark_red())

    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice.is_connected():
        voice.stop()
        await ctx.send(embed=stopped)
    else:
        await ctx.send(embed=error)


@bot.command(help="Leave the channel.", brief="Leave the channel.")
@commands.has_permissions(administrator=True)
async def leave(ctx):
    await ctx.message.delete()
    channel = ctx.message.author.voice.channel
    embed = discord.Embed(title="Music",
                           description=f"Trying to leave {channel}",
                           color=discord.Color.blue())

    suc = discord.Embed(title="Music",
                          description=f"Successfully left {channel} by {ctx.message.author}",
                          color=discord.Color.green())
    no = discord.Embed(title="Music",
                          description=f"Unsuccessfully left {channel}",
                          color=discord.Color.dark_red())

    base = await ctx.send(embed=embed)
    try:
        await ctx.voice_client.disconnect()
        await base.edit(embed=suc)
    except Exception:
        await base.edit(embed=no)

@leave.error
async def leave_error(error, ctx):
    if isinstance(error, commands.MissingPermissions):
        text = "Sorry {}, you do not have permissions to do that!".format(ctx.message.author)
        await ctx.send(text)



@bot.command(help="Add a number to a another number.",brief="Add a number to a another number.",)
async def add(ctx, left: int, right: int):
    msg1 = discord.Embed(title="Maths",
                        description=f"Thinking...",
                        color=discord.Color.green())
    ss = await ctx.send(embed=msg1)

    msg = discord.Embed(title="Maths",
                       description=f"The asnwer is {left + right}! Thanks for asking {ctx.message.author.mention}",
                       color=discord.Color.green())

    no = discord.Embed(title="Maths",
                        description=f"You forgot the numbers! {ctx.message.author.mention}",
                        color=discord.Color.green())

    await ctx.message.delete()

    if left & right is not None:
        await ss.edit(embed=msg)
    else:
        ctx.send(embed=no)


@bot.command(help="Prints the User pfp.", brief="Prints the User profile picture.")
async def user(ctx, *, member: discord.Member = None):
    await ctx.message.delete()
    if not member:
        member = ctx.message.author
    a = member.avatar_url
    await ctx.send(a)


@bot.command(pass_context=True, help="Shows the latency.", brief="Shows the latency.")
async def ping(ctx):
    wait = discord.Embed(title="Fun",
                        description=f"Waiting the server to respond!",
                        color=discord.Color.red())


    await ctx.message.delete()
    before = time.monotonic()
    message = await ctx.send(embed=wait)
    ping = (time.monotonic() - before) * 1000

    waited = discord.Embed(title="Fun",
                           description=f"Pong!  `{int(ping)}ms`",
                           color=discord.Color.green())
    await message.edit(embed=waited)
    print(f'Ping {int(ping)}ms')


@bot.command()
@commands.has_permissions(administrator=True)
async def console(ctx):
    times = int(input("Times you want to speak: "))
    await ctx.message.delete()
    for i in range(times):
        text = input("Speak now: ")
        while text == None:
            print("Slow")
        await ctx.send(text)



@bot.command(help="Says hello to you!", brief="Says a nice little hello back to you.")
async def hello(ctx):
    msg = discord.Embed(title="Fun",
                        description=f"Hello {ctx.author.name}",
                        color=discord.Color.green())
    await ctx.message.delete()
    async with ctx.typing():
        await asyncio.sleep(1)
    await ctx.send(embed=msg)


@bot.command(help="Says something what you like.", brief="Says something after the command")
async def say(ctx, *, text):
    msg = discord.Embed(title="Fun",
                        description=f'' + ctx.message.author.mention + ': ' + text,
                        color=discord.Color.green())

    await ctx.message.delete()
    await ctx.send(embed=msg)

@bot.command()
async def callarik(ctx):
    pev = input(f"{ctx.message.author} wants you to say something > ")
    while pev is None:
        time.sleep(1)
    await ctx.send(pev)




@bot.event
async def on_ready():
    print("Logging in...")
    print("Bot can now be used.")
    print("EnSave is mow on the use")
    print("----------------------")
    await bot.change_presence(activity=discord.Game('AriCC'))


bot.run('IM NOT STUPID')

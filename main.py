import discord
from discord.utils import get
from discord.ext import commands
from youtube_search import YoutubeSearch
from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option, create_choice
import youtube_dl
import time
import json
import os


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

#Coming Soon Commands


@bot.command()
async def noob(ctx, member: discord.Member):
    if member != None:
        await ctx.send(f"{member.mention} is noob.")
        await member.send("I know, I have been a noob lately...")
    else:
        await ctx.send("You forgot who!")


@bot.command()
async def react(ctx, reaction: str):
    if reaction != None:
        await ctx.send("comibng")
    else:
        await ctx.send("comibng")


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
    embed = discord.Embed(title="Your Gay?",
                          description="Yes, you are.",
                          color=discord.Color.magenta())
    await ctx.send(embed=embed)

#Working commands


@bot.command(pass_context=True, brief="This will play a song 'play [url]'", aliases=['pl'])
async def play(ctx, *, search):
    start = discord.Embed(title="Music", description="Trying to find your song!", color=discord.Color.purple())
    start1 = await ctx.send(embed=start)
    yt = YoutubeSearch(search, max_results=1).to_json()
    yt_id = str(json.loads(yt)['videos'][0]['id'])
    yt_url = 'https://www.youtube.com/watch?v=' + yt_id

    embed1 = discord.Embed(title="Music Link",
                          url=f'{yt_url}',
                          description="Is this what you wanted to hear?",
                          color=0xFF5733)
    await start1.edit(embed=embed1)

    embed2 = discord.Embed(title="Music",
                           description="Downloading the music for you!",
                           color=discord.Color.blue())

    embed3 = discord.Embed(title="Music",
                           description="Starting to play.",
                           color=discord.Color.dark_red())

    permission = discord.Embed(title="Music",
                           description='Wait for the current playing music end or use the "leave" command.',
                           color=discord.Color.red())

    stop = discord.Embed(title="Music",
                               description='Stopped playing the music!',
                               color=discord.Color.green())

    playing = discord.Embed(title="Music",
                         description='Currently playing the music!',
                         color=discord.Color.gold())

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send(embed=permission)
        return
    msg = await ctx.send(embed=embed2)
    print("Someone wants to play music let me get that ready for them...")
    voice = get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([yt_url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')
    await msg.edit(embed=embed3)
    voice_channel = ctx.author.voice.channel
    if voice_channel != None:
        vc = await voice_channel.connect()
        vc.play(discord.FFmpegPCMAudio(executable="C:/FFMPEG/ffmpeg.exe",
                                       source="D:/Desktop/Desktop/Modi Asiat/EnSave Reborn/song.mp3"))
        while vc.is_playing():
            await msg.edit(embed=playing)
        await vc.disconnect()
        await msg.edit(embed=stop)
    else:
        await ctx.send(str(ctx.author.name) + "is not in a channel.")


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
    await ctx.message.delete()
    await ctx.send(f'Changed the prefix to ' + prefix)
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)
    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@bot.command(help="Multiply numbers.", brief="Multiply numbers.")
async def multiply(ctx, left: int, right: int):
    await ctx.send(left * right)


@bot.command(help="Multiply numbers.", brief="Multiply numbers.")
async def remove(ctx, left: int, right: int):
    await ctx.send(left - right)


@bot.command(help="Divide numbers.", brief="Divide numbers.")
async def divide(ctx, left: int, right: int):
    await ctx.send(left / right)


@bot.command(pass_context=True, brief="Makes the bot join your channel", aliases=['j', 'jo'])
async def join(ctx):
    channel = ctx.message.author.voice.channel

    no_connect = discord.Embed(title="Music",
                          description="You are not connected to a voice channel",
                          color=discord.Color.dark_red())

    joined = discord.Embed(title="Music",
                              description=f"Joining {channel} to play the latest song.",
                              color=discord.Color.dark_red())
    plays = discord.Embed(title="Music",
                           description=f"Currently playing the latest song.",
                           color=discord.Color.green())
    stop = discord.Embed(title="Music",
                           description=f"Stopped playing the latest song.",
                           color=discord.Color.red())
    if not channel:
        await ctx.send(embed=no_connect)
        return
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await voice.disconnect()
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    msg = await ctx.send(embed=joined)

    voice.play(discord.FFmpegPCMAudio(executable="C:/FFMPEG/ffmpeg.exe", source="D:/Desktop/Desktop/Modi Asiat/EnSave Reborn/song.mp3"))
    while voice.is_playing():
        await msg.edit(embed=plays)
    await voice.disconnect()
    await msg.edit(embed=stop)


@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def nick(ctx, member: discord.Member, nick):
    await member.edit(nick=nick)
    await ctx.send(f'Nickname was changed for {member.mention} ')


@bot.command(help="Leave the channel.", brief="Leave the channel.", aliases=['stop', 'sto'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    embed = discord.Embed(title="Music",
                           description=f"Trying to leave {channel}",
                           color=discord.Color.blue())

    suc = discord.Embed(title="Music",
                          description=f"Successfully left {channel}",
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


@bot.command(help="Add a number to a another number.",brief="Add a number to a another number.",)
async def add(ctx, left: int, right: int):
    await ctx.send(left + right)


@bot.command(help="Prints the User pfp.", brief="Prints the User profile picture.")
async def user(ctx, *, member: discord.Member = None):
    await ctx.message.delete()
    if not member:
        member = ctx.message.author
    a = member.avatar_url
    await ctx.send(a)


@bot.command(pass_context=True, help="Shows the latency.", brief="Shows the latency.")
async def ping(ctx):
    await ctx.message.delete()
    before = time.monotonic()
    message = await ctx.send("Waiting the server to respond!")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f"Pong!  `{int(ping)}ms`")
    print(f'Ping {int(ping)}ms')


@bot.command(help="Says hello to you!", brief="Says a nice little hello back to you.")
async def hello(ctx):
    await ctx.message.delete()
    await ctx.send(f"Hello {ctx.author.name}!")


@bot.command(help="Prints a url image.", brief="Prints a url image.")
async def img(ctx, url):
    await ctx.message.delete()
    await ctx.send(f'' + ctx.message.author.mention)
    await ctx.send(url)


@bot.command(help="Says something what you like.", brief="Says something after the .say")
async def say(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(f'' + ctx.message.author.mention + ': ' + text)


@bot.event
async def on_ready():
    print('Bot is now working!')
    await bot.change_presence(activity=discord.Game('AriCC'))


bot.run('ODEyODA4ODY1NzI4OTU0Mzk5.YDGJPg.Utd09z1vSe2okDUgzZuHwMCW9xg')

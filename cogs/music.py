# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import datetime
import os

import aiohttp
import discord
import wavelink
from better_profanity import profanity
from discord.ext import commands
from dotenv import load_dotenv

from utils import db

load_dotenv()
host_server = str(os.getenv('MUSIC'))
host_pass = str(os.getenv('MUSIC_PASSWORD'))


# noinspection PyTypeChecker
class Music(commands.Cog, description="Play songs in voice channels"):
    EMOJI = "🎵"

    def __init__(self, bot):
        self.bot = bot

    # Create connect node task, when the bot is ready
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.loop.create_task(self.connect_nodes())

    # Connect the bot to a lavalink server
    async def connect_nodes(self) -> None:
        await wavelink.NodePool.create_node(bot=self.bot, host=host_server, port=2333, password=host_pass)

    # When a Wavelink node is ready this will be run
    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node) -> None:
        print(f"WaveLink node: {node.identifier} is ready.")

    # noinspection PyUnusedLocal
    # If there is more songs after the track ends, plays a new one
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track, reason) -> None:
        if not player.queue.is_empty:
            new = await player.queue.get_wait()
            await player.play(new)
        else:
            await player.stop()

    # When the bot joins a voice channel, it sets itself to be deafened
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member,
                                    before: discord.VoiceState,
                                    after: discord.VoiceState) -> None:
        if member.id == self.bot.user.id:
            if before.channel is None and after.channel is not None:
                await member.edit(deafen=True)

    # Command to play songs in a voice channel using YouTube
    @commands.command(name="play", aliases=['youtube', 'yt'], help="Play a song using YouTube.")
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack) -> None:
        if not ctx.author.voice:
            not_connected = discord.Embed(title="Music",
                                          description=f"You are not connected to a voice channel.",
                                          color=discord.Color.from_rgb(48, 50, 54),
                                          timestamp=datetime.datetime.utcnow())
            return await ctx.send(embed=not_connected)

        voice: wavelink.Player = ctx.voice_client or await ctx.author.voice.channel.connect(cls=wavelink.Player)

        if voice.queue.is_empty and not voice.is_playing():
            now_playing = discord.Embed(title="Queue",
                                        description=f'**Now playing**: [{profanity.censor(search.title)}]'
                                                    f'({search.uri})',
                                        color=discord.Color.from_rgb(48, 50, 54),
                                        timestamp=datetime.datetime.utcnow())
            now_playing.add_field(name="Author", value=f"{search.author}")
            await voice.play(search)
            await ctx.reply(embed=now_playing)
            return

        added_queue = discord.Embed(title="Queue",
                                    description=f"Added [{profanity.censor(search.title)}]"
                                                f"({search.uri}) to the queue.",
                                    color=discord.Color.from_rgb(48, 50, 54),
                                    timestamp=datetime.datetime.utcnow())
        added_queue.add_field(name="Author", value=f"{search.author}")

        await voice.queue.put_wait(search)
        await ctx.reply(embed=added_queue)
        if profanity.contains_profanity(search.title):
            await ctx.message.delete()

    # Command for connecting to a voice channel. You can specify the channel or not, so it joins the channel you are in
    @commands.command(name="connect", aliases=["join"], help="Connect to a voice channel")
    async def connect_command(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None) -> None:
        if channel:
            connected_success = discord.Embed(title="Music",
                                              description=f"Connected to `{channel.name}`",
                                              color=discord.Color.from_rgb(48, 50, 54),
                                              timestamp=datetime.datetime.utcnow())
            await channel.connect(cls=wavelink.Player)
            await ctx.send(embed=connected_success)
        else:
            if ctx.author.voice:
                connected_success = discord.Embed(title="Music",
                                                  description=f"Connected to `{ctx.author.voice.channel.name}`",
                                                  color=discord.Color.from_rgb(48, 50, 54),
                                                  timestamp=datetime.datetime.utcnow())
                await ctx.author.voice.channel.connect(cls=wavelink.Player)
                await ctx.send(embed=connected_success)
            else:
                not_connected = discord.Embed(title="Music",
                                              description=f"You are not connected to a voice channel.",
                                              color=discord.Color.from_rgb(48, 50, 54),
                                              timestamp=datetime.datetime.utcnow())
                return await ctx.send(embed=not_connected)

    # Command to leave from a voice channel
    @commands.command(name="disconnect", aliases=["leave"], help="Disconnect from a voice channel")
    async def disconnect_command(self, ctx: commands.Context) -> None:
        voice: wavelink.Player = ctx.voice_client
        if ctx.author.voice:
            if voice and voice.is_connected():
                disconnected = discord.Embed(title="Music",
                                             description=f"I have disconnected from `{ctx.author.voice.channel.name}`.",
                                             color=discord.Color.from_rgb(48, 50, 54),
                                             timestamp=datetime.datetime.utcnow())
                await voice.disconnect()
                return await ctx.send(embed=disconnected)
            else:
                not_connected = discord.Embed(title="Music",
                                              description=f"I am not in a voice channel.",
                                              color=discord.Color.from_rgb(48, 50, 54),
                                              timestamp=datetime.datetime.utcnow())
                await ctx.send(embed=not_connected)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"You are not connected to the voice channel.",
                                          color=discord.Color.from_rgb(48, 50, 54),
                                          timestamp=datetime.datetime.utcnow())
            return await ctx.send(embed=not_connected)

    # Command for pausing your songs
    @commands.command(name="pause", help="Pause voice channel")
    async def pause_command(self, ctx: commands.Context) -> None:
        voice: wavelink.Player = ctx.voice_client
        if ctx.author.voice:
            if voice and voice.is_connected():
                if voice.is_paused():
                    paused_already = discord.Embed(title="Queue",
                                                   description=f"I am already paused.",
                                                   color=discord.Color.from_rgb(48, 50, 54),
                                                   timestamp=datetime.datetime.utcnow())
                    return await ctx.send(embed=paused_already)

                paused = discord.Embed(title="Queue",
                                       description=f"The playback has been paused.",
                                       color=discord.Color.from_rgb(48, 50, 54),
                                       timestamp=datetime.datetime.utcnow())
                await voice.pause()
                await ctx.send(embed=paused)
            else:
                not_connected = discord.Embed(title="Music",
                                              description=f"I am not in a voice channel.",
                                              color=discord.Color.from_rgb(48, 50, 54),
                                              timestamp=datetime.datetime.utcnow())
                await ctx.send(embed=not_connected)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"You are not connected to the voice channel.",
                                          color=discord.Color.from_rgb(48, 50, 54),
                                          timestamp=datetime.datetime.utcnow())
            return await ctx.send(embed=not_connected)

    # Command to resume listening to your songs
    @commands.command(name="resume", help="Resume voice channel")
    async def resume_command(self, ctx: commands.Context) -> None:
        voice: wavelink.Player = ctx.voice_client
        if ctx.author.voice:
            if voice and voice.is_connected():
                if voice.is_paused():
                    resumed = discord.Embed(title="Queue",
                                            description=f"The playback has been resumed.",
                                            color=discord.Color.from_rgb(48, 50, 54),
                                            timestamp=datetime.datetime.utcnow())
                    await voice.resume()
                    await ctx.send(embed=resumed)
                else:
                    resumed = discord.Embed(title="Queue",
                                            description=f"I am not paused.",
                                            color=discord.Color.from_rgb(48, 50, 54),
                                            timestamp=datetime.datetime.utcnow())
                    await ctx.send(embed=resumed)
            else:
                not_connected = discord.Embed(title="Music",
                                              description=f"I am not in a voice channel.",
                                              color=discord.Color.from_rgb(48, 50, 54),
                                              timestamp=datetime.datetime.utcnow())
                await ctx.send(embed=not_connected)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"You are not connected to the voice channel.",
                                          color=discord.Color.from_rgb(48, 50, 54),
                                          timestamp=datetime.datetime.utcnow())
            return await ctx.send(embed=not_connected)

    # Command to stop the music and clear the queue
    @commands.command(name="stop", help="Stops the current song and clears the queue")
    async def stop_command(self, ctx: commands.Context) -> None:
        voice: wavelink.Player = ctx.voice_client
        if ctx.author.voice and voice:
            if voice.is_playing() | voice.is_paused():
                stopped = discord.Embed(title="Queue",
                                        description=f"The playback has been stopped and the queue has been cleared.",
                                        color=discord.Color.from_rgb(48, 50, 54),
                                        timestamp=datetime.datetime.utcnow())

                # This will clear the queue and stop the player
                voice.queue.clear()
                await voice.stop()

                await ctx.send(embed=stopped)
            else:
                not_connected = discord.Embed(title="Queue",
                                              description=f"Music isn't playing.",
                                              color=discord.Color.from_rgb(48, 50, 54),
                                              timestamp=datetime.datetime.utcnow())
                await ctx.send(embed=not_connected)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"We are not connected to the voice channel.",
                                          color=discord.Color.from_rgb(48, 50, 54),
                                          timestamp=datetime.datetime.utcnow())
            return await ctx.send(embed=not_connected)

    # Command to change the volume of the player
    @commands.command(name="volume", description="Change the volume of the player",
                      help="Change the volume of the player")
    async def volume_command(self, ctx: commands.Context, volume: int):
        voice: wavelink.Player = ctx.voice_client
        if ctx.author.voice:
            if voice and voice.is_connected():
                if volume < 0 or volume > 100:
                    volume_must = discord.Embed(title="Music",
                                                description="Volume must be between 0 and 100",
                                                color=discord.Color.from_rgb(48, 50, 54),
                                                timestamp=datetime.datetime.utcnow())
                    return await ctx.send(embed=volume_must)
                if ctx.author.voice:
                    changed_volume = discord.Embed(title="Music",
                                                   description=f"Changed volume to **{volume}**%",
                                                   color=discord.Color.from_rgb(48, 50, 54),
                                                   timestamp=datetime.datetime.utcnow())
                    await voice.set_volume(volume)
                    await ctx.send(embed=changed_volume)

            else:
                not_connected = discord.Embed(title="Queue",
                                              description=f"Music isn't playing.",
                                              color=discord.Color.from_rgb(48, 50, 54),
                                              timestamp=datetime.datetime.utcnow())
                await ctx.send(embed=not_connected)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"You are not connected to the voice channel.",
                                          color=discord.Color.from_rgb(48, 50, 54),
                                          timestamp=datetime.datetime.utcnow())
            return await ctx.send(embed=not_connected)

    # Command to shuffle the order of tracks. This command is limited to premium users
    @commands.command(name="shuffle", help="Shuffle the queue.")
    async def shuffle_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if ctx.author.voice and voice:
            if db.get_user_premium(ctx.author.id):
                if not voice.is_playing():
                    not_connected = discord.Embed(title="Queue",
                                                  description="Music isn't playing.",
                                                  color=discord.Color.from_rgb(48, 50, 54),
                                                  timestamp=datetime.datetime.utcnow())
                    return await ctx.send(embed=not_connected)
                if not voice.queue():
                    no_tracks = discord.Embed(title="Queue",
                                              description=f"No tracks are queued for **{ctx.guild.name}**",
                                              color=discord.Color.from_rgb(48, 50, 54),
                                              timestamp=datetime.datetime.utcnow())
                    return await ctx.send(embed=no_tracks)
                voice.queue.shuffle()
                shuffle = discord.Embed(title="Queue",
                                        description=f"Shuffled the queue for **{ctx.guild.name}**",
                                        color=discord.Color.from_rgb(48, 50, 54),
                                        timestamp=datetime.datetime.utcnow())
                await ctx.send(embed=shuffle)
            else:
                premium = discord.Embed(title="EnSave Premium",
                                        description="You need to be a premium member of this to use this command.",
                                        color=discord.Color.from_rgb(48, 50, 54),
                                        timestamp=datetime.datetime.utcnow())
                return await ctx.send(embed=premium)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"You are not connected to the voice channel.",
                                          color=discord.Color.from_rgb(48, 50, 54),
                                          timestamp=datetime.datetime.utcnow())
            return await ctx.send(embed=not_connected)

    # Command to see information about the current track.
    @commands.command(name="playing", help="Info about the current track.")
    async def playing_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if voice.queue:
            song = await voice.queue.get()
            embed = discord.Embed(title="Queue",
                                  description=f"**{song.title}**\n\n"
                                  )
            if isinstance(song, wavelink.YouTubeTrack):
                embed.set_thumbnail(url=song.thumbnail)
            embed.add_field(name="Author", value=song.author)
            await ctx.send(embed=embed)
        else:
            no_tracks = discord.Embed(title="Queue",
                                      description=f"No tracks are queued for **{ctx.guild.name}**",
                                      color=discord.Color.from_rgb(48, 50, 54),
                                      timestamp=datetime.datetime.utcnow())
            await ctx.send(embed=no_tracks)

    # Command to skip songs
    @commands.command(name="skip", help="Skips the current song.")
    async def skip_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if ctx.author.voice:
            if not voice.queue.is_empty:
                await voice.stop()
                skipped = discord.Embed(title="Queue",
                                        description=f"The song has been skipped and now playing {voice.queue[0]}",
                                        color=discord.Color.from_rgb(48, 50, 54),
                                        timestamp=datetime.datetime.utcnow())
                return await ctx.send(embed=skipped, delete_after=5)
            else:
                not_connected = discord.Embed(title="Queue",
                                              description=f"Queue might be empty.",
                                              color=discord.Color.from_rgb(48, 50, 54),
                                              timestamp=datetime.datetime.utcnow())
                await ctx.send(embed=not_connected)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"We are not connected to the voice channel.",
                                          color=discord.Color.from_rgb(48, 50, 54),
                                          timestamp=datetime.datetime.utcnow())
            return await ctx.send(embed=not_connected)

    @commands.command(name="lyrics", help="Gets the lyrics of the current track.")
    async def lyrics_command(self, ctx, name=None):
        voice: wavelink.Player = ctx.voice_client
        if not name:
            if voice.is_playing():
                name = voice.source.title

        async with ctx.typing():
            async with aiohttp.request("GET", "https://some-random-api.ml/lyrics?title=" + name, headers={}) as r:
                if not 200 <= r.status <= 299:
                    return await ctx.send("Could not found anything.")

                data = await r.json()

                if len(data["lyrics"]) > 2000:
                    embed2 = discord.Embed(
                        title=data["title"],
                        description=f"<{data['links']['genius']}>",
                        colour=ctx.author.colour,
                        timestamp=datetime.datetime.utcnow())
                    return await ctx.send(embed=embed2)

                embed = discord.Embed(
                    title=data["title"],
                    description=data["lyrics"],
                    colour=ctx.author.colour,
                    timestamp=datetime.datetime.utcnow())
                embed.set_thumbnail(url=data["thumbnail"]["genius"])
                embed.set_author(name=data["author"])
                await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Music(bot))

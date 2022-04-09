# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import os

import discord
import wavelink
from better_profanity import profanity
from discord.ext import commands
from dotenv import load_dotenv

from utils import database

load_dotenv()
host_server = str(os.getenv('MUSIC'))
host_pass = str(os.getenv('MUSIC_PASSWORD'))


# noinspection PyTypeChecker
class Music(commands.Cog, description="Music"):
    EMOJI = "🎵"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.connect_nodes())

    async def connect_nodes(self):
        await wavelink.NodePool.create_node(bot=self.bot, host=host_server, port=2333, password=host_pass)

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"WaveLink node: {node.identifier} is ready.")

    # noinspection PyUnusedLocal
    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track, reason):
        if not player.queue.is_empty:
            new = player.queue.get()
            await player.play(new)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member,
                                    before: discord.VoiceState,
                                    after: discord.VoiceState):
        if member.id == self.bot.user.id:
            if before.channel is None and after.channel is not None:
                await member.edit(deafen=True)

    @commands.command(name="play", aliases=['youtube', 'yt'], help="Play a song.")
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            voice: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            voice: wavelink.Player = ctx.voice_client

        if not ctx.author.voice:
            not_connected = discord.Embed(title="Music",
                                          description=f"You are not connected to a voice channel.",
                                          color=ctx.author.color,
                                          timestamp=database.get_time())
            return await ctx.send(embed=not_connected)

        if voice.queue.is_empty and not voice.is_playing():
            now_playing = discord.Embed(title="Music",
                                        description=f'**Now playing**: [{profanity.censor(search.title)}]'
                                                    f'({search.uri})',
                                        color=ctx.author.color,
                                        timestamp=database.get_time())
            now_playing.set_thumbnail(url=search.thumbnail)
            now_playing.add_field(name="Author", value=f"{search.author}")

            await voice.play(search)
            await ctx.reply(embed=now_playing)
        else:
            added_queue = discord.Embed(title="Music",
                                        description=f"Added [{profanity.censor(search.title)}]"
                                                    f"({search.uri}) to the queue.",
                                        color=ctx.author.color,
                                        timestamp=database.get_time())
            added_queue.set_thumbnail(url=search.thumbnail)
            added_queue.add_field(name="Author", value=f"{search.author}")

            await voice.queue.put_wait(search)
            await ctx.reply(embed=added_queue)
        if profanity.contains_profanity(search.title):
            await ctx.message.delete()

    @commands.command(name="soundcloud", aliases=['sc'], help="Play a song using soundcloud.")
    async def soundcloud(self, ctx: commands.Context, *, search: wavelink.SoundCloudTrack):
        if not ctx.voice_client:
            voice: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            voice: wavelink.Player = ctx.voice_client

        if not ctx.author.voice:
            not_connected = discord.Embed(title="Music",
                                          description=f"You are not connected to a voice channel.",
                                          color=ctx.author.color,
                                          timestamp=database.get_time())
            return await ctx.send(embed=not_connected)

        if voice.queue.is_empty and not voice.is_playing():
            now_playing = discord.Embed(title="Music",
                                        description=f'**Now playing**: [{profanity.censor(search.title)}]'
                                                    f'({search.uri})',
                                        color=ctx.author.color,
                                        timestamp=database.get_time())
            now_playing.add_field(name="Author", value=f"{search.author}")

            await voice.play(search)
            await ctx.reply(embed=now_playing)
        else:
            added_queue = discord.Embed(title="Music",
                                        description=f"Added [{profanity.censor(search.title)}]"
                                                    f"({search.uri}) to the queue.",
                                        color=ctx.author.color,
                                        timestamp=database.get_time())
            added_queue.add_field(name="Author", value=f"{search.author}")

            await voice.queue.put_wait(search)
            await ctx.reply(embed=added_queue)
        if profanity.contains_profanity(search.title):
            await ctx.message.delete()

    @commands.command(name="connect", aliases=["join"], help="Connect to a voice channel")
    async def connect_command(self, ctx: commands.Context, *, channel: discord.VoiceChannel = None):
        voice: wavelink.Player = ctx.voice_client
        connected_success = discord.Embed(title="Music",
                                          description=f"Connected to `{ctx.author.voice.channel.name}`",
                                          color=ctx.author.color,
                                          timestamp=database.get_time())
        if not voice:
            if channel:
                await channel.connect(cls=wavelink.Player)
                return await ctx.send(embed=connected_success)
            elif ctx.author.voice is not None:
                await ctx.author.voice.channel.connect(cls=wavelink.Player)
                return await ctx.send(embed=connected_success)
        else:
            connected_already = discord.Embed(title="Music",
                                              description="I'm already connected to a voice channel.",
                                              color=ctx.author.color,
                                              timestamp=database.get_time())
            return await ctx.reply(embed=connected_already)
        not_connected = discord.Embed(title="Music",
                                      description=f"You aren't connected to a voice channel",
                                      color=ctx.author.color,
                                      timestamp=database.get_time())
        return await ctx.send(embed=not_connected)

    @commands.command(name="disconnect", aliases=["leave"], help="Disconnect from a voice channel")
    async def disconnect_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if voice and voice.is_connected():
            if not ctx.author.voice:
                not_connected = discord.Embed(title="Music",
                                              description=f"You are not connected to a voice channel.",
                                              color=ctx.author.color,
                                              timestamp=database.get_time())
                return ctx.send(embed=not_connected)
            if ctx.author.voice.channel == voice.channel:
                disconnected = discord.Embed(title="Music",
                                             description=f"I have disconnected from `{ctx.author.voice.channel.name}`.",
                                             color=ctx.author.color,
                                             timestamp=database.get_time())
                await voice.disconnect()
                return await ctx.send(embed=disconnected)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"I am not in a voice channel.",
                                          color=ctx.author.color,
                                          timestamp=database.get_time())
            await ctx.send(embed=not_connected)

    @commands.command(name="pause", help="Pause voice channel")
    async def pause_command(self, ctx: commands.Context):
        view = database.Resume()
        voice: wavelink.Player = ctx.voice_client
        if voice and voice.is_connected():
            if not ctx.author.voice:
                not_connected = discord.Embed(title="Music",
                                              description=f"You are not connected to a voice channel.",
                                              color=ctx.author.color,
                                              timestamp=database.get_time())
                return ctx.send(embed=not_connected)
            if voice.is_paused():
                paused_already = discord.Embed(title="Music",
                                               description=f"I am already paused.",
                                               color=ctx.author.color,
                                               timestamp=database.get_time())
                return await ctx.send(embed=paused_already)

            paused = discord.Embed(title="Music",
                                   description=f"The playback has been paused.",
                                   color=ctx.author.color,
                                   timestamp=database.get_time())
            await voice.pause()
            await ctx.send(embed=paused, view=view)
            await view.wait()
            if view.value is None:
                return
            elif view.value:
                await voice.resume()
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"I am not in a voice channel.",
                                          color=ctx.author.color,
                                          timestamp=database.get_time())
            await ctx.send(embed=not_connected)

    @commands.command(name="resume", help="Resume voice channel")
    async def resume_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if voice and voice.is_connected():
            if not ctx.author.voice:
                not_connected = discord.Embed(title="Music",
                                              description=f"You are not connected to a voice channel.",
                                              color=ctx.author.color,
                                              timestamp=database.get_time())
                return ctx.send(embed=not_connected)
            if voice.is_paused():
                resumed = discord.Embed(title="Music",
                                        description=f"The playback has been resumed.",
                                        color=ctx.author.color,
                                        timestamp=database.get_time())
                await voice.resume()
                await ctx.send(embed=resumed)
            else:
                resumed = discord.Embed(title="Music",
                                        description=f"I am not paused.",
                                        color=ctx.author.color,
                                        timestamp=database.get_time())
                await ctx.send(embed=resumed)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"I am not in a voice channel.",
                                          color=ctx.author.color,
                                          timestamp=database.get_time())
            await ctx.send(embed=not_connected)

    @commands.command(name="stop", help="Stops the current song and clears the queue")
    async def stop_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if voice.is_playing():
            if ctx.author.voice:
                stopped = discord.Embed(title="Music",
                                        description=f"The playback has been stopped and the queue has been cleared.",
                                        color=ctx.author.color,
                                        timestamp=database.get_time())

                # Clears the queue and stops the player
                voice.queue.clear()
                await voice.stop()
                await ctx.send(embed=stopped)
            else:
                not_connected = discord.Embed(title="Music",
                                              description=f"You are not connected to the voice channel.",
                                              color=ctx.author.color,
                                              timestamp=database.get_time())
                await ctx.send(embed=not_connected)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"Music isn't playing.",
                                          color=ctx.author.color,
                                          timestamp=database.get_time())
            await ctx.send(embed=not_connected)

    @commands.command(name="volume", description="Change the volume of the player",
                      help="Change the volume of the player")
    async def volume_command(self, ctx: commands.Context, volume: int):
        voice: wavelink.Player = ctx.voice_client
        if voice and voice.is_connected():
            if not ctx.author.voice:
                not_connected = discord.Embed(title="Music",
                                              description=f"You are not connected to the voice channel.",
                                              color=ctx.author.color,
                                              timestamp=database.get_time())
                return await ctx.send(embed=not_connected)
            elif volume < 0 or volume > 100:
                volume_must = discord.Embed(title="Music",
                                            description="Volume must be between 0 and 100",
                                            color=ctx.author.color,
                                            timestamp=database.get_time())
                return await ctx.send(embed=volume_must)
            if ctx.author.voice:
                changed_volume = discord.Embed(title="Music",
                                               description=f"Changed volume to **{volume}**%",
                                               color=ctx.author.color,
                                               timestamp=database.get_time())
                await voice.set_volume(volume)
                await ctx.send(embed=changed_volume)

        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"Music isn't playing.",
                                          color=ctx.author.color,
                                          timestamp=database.get_time())
            await ctx.send(embed=not_connected)

    @commands.command(name="shuffle", help="Shuffle the queue.")
    async def shuffle_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if database.get_premium(ctx.author.id):
            if ctx.author.voice:
                not_connected = discord.Embed(title="Music",
                                              description=f"You are not connected to the voice channel.",
                                              color=ctx.author.color,
                                              timestamp=database.get_time())
                return await ctx.send(embed=not_connected)
            elif not ctx.voice_client:
                not_connected = discord.Embed(title="Music",
                                              description="Music isn't playing.",
                                              color=ctx.author.color,
                                              timestamp=database.get_time())
                return await ctx.send(embed=not_connected)
            elif not voice.queue():
                no_tracks = discord.Embed(title="Music",
                                          description=f"No tracks are queued for **{ctx.guild.name}**",
                                          color=ctx.author.color,
                                          timestamp=database.get_time())
                return await ctx.send(embed=no_tracks)
            else:
                voice.queue.shuffle()
                shuffle = discord.Embed(title="Music",
                                        description=f"Shuffled the queue for **{ctx.guild.name}**",
                                        color=ctx.author.color,
                                        timestamp=database.get_time())
                await ctx.send(embed=shuffle)

    @commands.command(name="playing", help="Info about the current track.")
    async def playing_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        song = await voice.queue.get()
        if voice.is_playing():
            embed = discord.Embed(title="Music",
                                  description=f"**{song.title}**\n\n"
                                  )
            if isinstance(song, wavelink.YouTubeTrack):
                embed.set_thumbnail(url=song.thumbnail)
            embed.add_field(name="Author", value=song.author)
            await ctx.send(embed=embed)
        else:
            no_tracks = discord.Embed(title="Music",
                                      description=f"No tracks are queued for **{ctx.guild.name}**",
                                      color=ctx.author.color,
                                      timestamp=database.get_time())
            await ctx.send(embed=no_tracks)

    @commands.command(name="skip", help="Skips the song.")
    async def skip_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if voice.is_playing():
            if not ctx.author.voice:
                not_connected = discord.Embed(title="Music",
                                              description=f"You are not connected to the voice channel.",
                                              color=ctx.author.color,
                                              timestamp=database.get_time())
                return ctx.send(embed=not_connected)
            else:
                skipped = discord.Embed(title="Music",
                                        description=f"The song has been skipped.",
                                        color=ctx.author.color,
                                        timestamp=database.get_time())
                await voice.stop()
                return await ctx.send(embed=skipped)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"Music isn't playing.",
                                          color=ctx.author.color,
                                          timestamp=database.get_time())
            await ctx.send(embed=not_connected)


async def setup(bot):
    await bot.add_cog(Music(bot))

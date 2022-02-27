# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import nextcord
import nextlink as wavelink
from better_profanity import profanity
from nextcord.ext import commands

from utils import db


# noinspection PyTypeChecker
class Music(commands.Cog, description="Music commands"):
    COG_EMOJI = "🎵"

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.loop.create_task(self.connect_nodes())
        self.loop = False

    async def connect_nodes(self):
        await self.bot.wait_until_ready()

        await wavelink.NodePool.create_node(bot=self.bot,
                                            host='127.0.0.1',
                                            port=2333,
                                            password='thisisarik')

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f" Wavelink node: {node.identifier} is ready.")

    @commands.Cog.listener()
    async def on_wavelink_track_end(self, player: wavelink.Player, track, reason):
        if not self.loop:
            if not player.queue.is_empty:
                new = player.queue.get()
                await player.play(new)
        if self.loop:
            await player.play(player.track)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: nextcord.Member,
                                    before: nextcord.VoiceState,
                                    after: nextcord.VoiceState):
        if member.id == self.bot.user.id:
            if before.channel is None and after.channel is not None:
                await member.edit(deafen=True)

    @commands.command(name="play", aliases=['youtube', 'yt'], help="Play a song.")
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        view = db.PauseStop()
        if not ctx.voice_client:
            voice: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            voice: wavelink.Player = ctx.voice_client

        if not ctx.author.voice:
            not_connected = nextcord.Embed(title="Music",
                                           description=f"You are not connected to a voice channel.",
                                           color=ctx.author.color,
                                           timestamp=db.get_time())
            return ctx.send(embed=not_connected)

        if voice.queue.is_empty and not voice.is_playing():
            now_playing = nextcord.Embed(title="Music",
                                         description=f'**Now playing**: [{profanity.censor(search.title)}]'
                                                     f'({search.uri})',
                                         color=ctx.author.color,
                                         timestamp=db.get_time())
            now_playing.set_image(url=search.thumbnail)
            now_playing.add_field(name="Author", value=f"{search.author}")

            await voice.play(search)
            await ctx.reply(embed=now_playing, view=view)
            await view.wait()
            if view.value is None:
                return
            elif view.value == "pause":
                await voice.set_pause(True)

            elif view.value == "stop":
                await voice.stop()
        else:
            added_queue = nextcord.Embed(title="Music",
                                         description=f"Added [{profanity.censor(search.title)}]"
                                                     f"({search.uri}) to the queue.",
                                         color=ctx.author.color,
                                         timestamp=db.get_time())
            added_queue.set_image(url=search.thumbnail)
            await voice.queue.put_wait(search)
            await ctx.reply(embed=added_queue, view=view)
            await view.wait()
            if view.value is None:
                return view.clear_items()
            elif view.value == "pause":
                await voice.pause()
            elif view.value == "stop":
                await voice.stop()
        if profanity.contains_profanity(search.title):
            await ctx.message.delete()

    @commands.command(name="soundcloud", aliases=['sc'], help="Play a song using soundcloud.")
    async def soundcloud(self, ctx: commands.Context, *, search: wavelink.SoundCloudTrack):
        view = db.PauseStop()
        if not ctx.voice_client:
            voice: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            voice: wavelink.Player = ctx.voice_client

        if not ctx.author.voice:
            not_connected = nextcord.Embed(title="Music",
                                           description=f"You are not connected to a voice channel.",
                                           color=ctx.author.color,
                                           timestamp=db.get_time())
            return ctx.send(embed=not_connected)

        if voice.queue.is_empty and not voice.is_playing():
            now_playing = nextcord.Embed(title="Music",
                                         description=f'**Now playing**: [{profanity.censor(search.title)}]'
                                                     f'({search.uri})',
                                         color=ctx.author.color,
                                         timestamp=db.get_time())
            now_playing.add_field(name="Author", value=f"{search.author}")
            await voice.play(search)
            await ctx.reply(embed=now_playing, view=view)
            await view.wait()
            if view.value is None:
                return
            elif view.value == "pause":
                await voice.set_pause(True)

            elif view.value == "stop":
                await voice.stop()
        else:
            added_queue = nextcord.Embed(title="Music",
                                         description=f"Added [{profanity.censor(search.title)}]"
                                                     f"({search.uri}) to the queue.",
                                         color=ctx.author.color,
                                         timestamp=db.get_time())
            added_queue.add_field(name="Author", value=f"{search.author}")
            await voice.queue.put_wait(search)
            await ctx.reply(embed=added_queue, view=view)
            await view.wait()
            if view.value is None:
                return view.clear_items()
            elif view.value == "pause":
                await voice.pause()
            elif view.value == "stop":
                await voice.stop()
        if profanity.contains_profanity(search.title):
            await ctx.message.delete()

    @commands.command(name="connect", aliases=["join"], help="Connect to a voice channel")
    async def connect_command(self, ctx: commands.Context, *, channel: nextcord.VoiceChannel = None):
        voice: wavelink.Player = ctx.voice_client
        connected_success = nextcord.Embed(title="Music",
                                           description=f"Connected to `{ctx.author.voice.channel.name}`",
                                           color=ctx.author.color,
                                           timestamp=db.get_time())
        if not voice:
            if channel:
                await channel.connect(cls=wavelink.Player)
                return await ctx.send(embed=connected_success)
            elif ctx.author.voice is not None:
                await ctx.author.voice.channel.connect(cls=wavelink.Player)
                return await ctx.send(embed=connected_success)
        else:
            connected_already = nextcord.Embed(title="Music",
                                               description="I'm already connected to a voice channel.",
                                               color=ctx.author.color,
                                               timestamp=db.get_time())
            return await ctx.reply(embed=connected_already)
        not_connected = nextcord.Embed(title="Music",
                                       description=f"You aren't connected to a voice channel",
                                       color=ctx.author.color,
                                       timestamp=db.get_time())
        return await ctx.send(embed=not_connected)

    @commands.command(name="disconnect", aliases=["leave"], help="Disconnect from a voice channel")
    async def disconnect_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if voice and voice.is_connected():
            if not ctx.author.voice:
                not_connected = nextcord.Embed(title="Music",
                                               description=f"You are not connected to a voice channel.",
                                               color=ctx.author.color,
                                               timestamp=db.get_time())
                return ctx.send(embed=not_connected)
            disconnected = nextcord.Embed(title="Music",
                                          description=f"I have disconnected.",
                                          color=ctx.author.color,
                                          timestamp=db.get_time())
            await voice.disconnect()
            return await ctx.send(embed=disconnected)
        not_connected = nextcord.Embed(title="Music",
                                       description=f"I am not to a voice channel.",
                                       color=ctx.author.color,
                                       timestamp=db.get_time())
        await ctx.send(embed=not_connected)

    @commands.command(name="pause", help="Pause voice channel")
    async def pause_command(self, ctx: commands.Context):
        view = db.Resume()
        voice: wavelink.Player = ctx.voice_client
        if voice and voice.is_connected():
            if not ctx.author.voice:
                not_connected = nextcord.Embed(title="Music",
                                               description=f"You are not connected to a voice channel.",
                                               color=ctx.author.color,
                                               timestamp=db.get_time())
                return ctx.send(embed=not_connected)
            if voice.is_paused():
                paused_already = nextcord.Embed(title="Music",
                                                description=f"I am already paused.",
                                                color=ctx.author.color,
                                                timestamp=db.get_time())
                return await ctx.send(embed=paused_already)
            paused = nextcord.Embed(title="Music",
                                    description=f"The playback has been paused.",
                                    color=ctx.author.color,
                                    timestamp=db.get_time())
            await voice.pause()
            await ctx.send(embed=paused, view=view)
            await view.wait()
            if view.value is None:
                return
            elif view.value:
                await voice.resume()

        not_connected = nextcord.Embed(title="Music",
                                       description=f"I am not to a voice channel.",
                                       color=ctx.author.color,
                                       timestamp=db.get_time())
        await ctx.send(embed=not_connected)

    @commands.command(name="resume", help="Resume voice channel")
    async def resume_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if voice and voice.is_connected():
            if not ctx.author.voice:
                not_connected = nextcord.Embed(title="Music",
                                               description=f"You are not connected to a voice channel.",
                                               color=ctx.author.color,
                                               timestamp=db.get_time())
                return ctx.send(embed=not_connected)
            if voice.is_paused():
                resumed = nextcord.Embed(title="Music",
                                         description=f"The playback has been resumed.",
                                         color=ctx.author.color,
                                         timestamp=db.get_time())
                await voice.resume()
                return await ctx.send(embed=resumed)
            resumed = nextcord.Embed(title="Music",
                                     description=f"I am not paused.",
                                     color=ctx.author.color,
                                     timestamp=db.get_time())
            return await ctx.send(embed=resumed)
        not_connected = nextcord.Embed(title="Music",
                                       description=f"I am not to a voice channel.",
                                       color=ctx.author.color,
                                       timestamp=db.get_time())
        await ctx.send(embed=not_connected)

    @commands.command(name="stop", help="Stops the current song and clears the queue")
    async def stop_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if voice.is_playing():
            if voice.channel != ctx.author.voice.channel:
                not_connected = nextcord.Embed(title="Music",
                                               description=f"You are not connected to the voice channel.",
                                               color=ctx.author.color,
                                               timestamp=db.get_time())
                return ctx.send(embed=not_connected)
            stopped = nextcord.Embed(title="Music",
                                     description=f"The playback has been stopped and the queue has been cleared.",
                                     color=ctx.author.color,
                                     timestamp=db.get_time())
            voice.queue.clear()
            await voice.stop()
            return await ctx.send(embed=stopped)
        not_connected = nextcord.Embed(title="Music",
                                       description=f"I am not to a voice channel.",
                                       color=ctx.author.color,
                                       timestamp=db.get_time())
        await ctx.send(embed=not_connected)

    @commands.command(name="volume", description="Change the volume of the player",
                      help="Change the volume of the player")
    async def volume_command(self, ctx: commands.Context, volume: int):
        voice: wavelink.Player = ctx.voice_client
        if voice and voice.is_connected():
            if voice.channel != ctx.author.voice.channel:
                not_connected = nextcord.Embed(title="Music",
                                               description=f"You are not connected to the voice channel.",
                                               color=ctx.author.color,
                                               timestamp=db.get_time())
                return ctx.send(embed=not_connected)
            if volume < 0 or volume > 100:
                volume_must = nextcord.Embed(title="Music",
                                             description="Volume must be between 0 and 100",
                                             color=ctx.author.color,
                                             timestamp=db.get_time())
                return await ctx.send(embed=volume_must)
            changed_volume = nextcord.Embed(title="Music",
                                            description=f"Changed volume to **{volume}**%",
                                            color=ctx.author.color,
                                            timestamp=db.get_time())
            await voice.set_volume(volume)
            return await ctx.send(embed=changed_volume)
        not_connected = nextcord.Embed(title="Music",
                                       description=f"I am not to a voice channel.",
                                       color=ctx.author.color,
                                       timestamp=db.get_time())
        await ctx.send(embed=not_connected)

    @commands.command(name="loop", help="Make the song loop.")
    async def loop_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if db.get_premium(ctx.author.id):
            if voice.channel != ctx.author.voice.channel:
                not_connected = nextcord.Embed(title="Music",
                                               description=f"You are not connected to the voice channel.",
                                               color=ctx.author.color,
                                               timestamp=db.get_time())
                return ctx.send(embed=not_connected)
            if not ctx.voice_client:
                not_connected = nextcord.Embed(title="Music",
                                               description="I am not connected to a voice channel",
                                               color=ctx.author.color,
                                               timestamp=db.get_time())
                return await ctx.send(embed=not_connected)
            if not voice.is_playing():
                no_tracks = nextcord.Embed(title="Music",
                                           description=f"No tracks are queued for **{ctx.guild.name}**",
                                           color=ctx.author.color,
                                           timestamp=db.get_time())
                return await ctx.send(embed=no_tracks)
            self.loop ^= True
            if self.loop:
                loop_enabled = nextcord.Embed(title="Music",
                                              description="Looping has been enabled",
                                              color=ctx.author.color,
                                              timestamp=db.get_time())
                return await ctx.send(embed=loop_enabled)
            else:
                loop_disabled = nextcord.Embed(title="Music",
                                               description="Looping has been disabled",
                                               color=ctx.author.color,
                                               timestamp=db.get_time())
                return await ctx.send(embed=loop_disabled)

        await ctx.reply(embed=db.premium_embed(ctx, "Music"))


def setup(bot):
    bot.add_cog(Music(bot))

# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import nextcord
import nextlink as wavelink
from nextcord.ext import commands

from utils import getter


# noinspection PyTypeChecker
class Music(commands.Cog, description="Music commands"):
    COG_EMOJI = "🎵"

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        bot.loop.create_task(self.connect_nodes())

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
    async def on_wavelink_track_end(self, player: wavelink.Player, **payload: dict):
        if not player.queue.is_empty:
            new = player.queue.get()
            await player.play(new)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: nextcord.Member,
                                    before: nextcord.VoiceState,
                                    after: nextcord.VoiceState):
        if member.id == self.bot.user.id:
            if before.channel is None and after.channel is not None:
                await member.edit(deafen=True)

    @commands.command(name="play", help="Play a song.")
    async def play(self, ctx: commands.Context, *, search: wavelink.YouTubeTrack):
        if not ctx.voice_client:
            voice: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            voice: wavelink.Player = ctx.voice_client

        if voice.queue.is_empty and not voice.is_playing():
            now_playing = nextcord.Embed(title="Music",
                                         description=f'**Now playing**: `{search.title}`',
                                         color=ctx.author.color,
                                         timestamp=getter.get_time())
            await voice.play(search)
            return await ctx.send(embed=now_playing)
        else:
            added_queue = nextcord.Embed(title="Music",
                                         description=f"Added `{search.title}` to the queue.",
                                         color=ctx.author.color,
                                         timestamp=getter.get_time())
            await voice.queue.put_wait(search)
            return await ctx.send(embed=added_queue)

    @commands.command(name="connect", aliases=["join"], help="Connect to a voice channel")
    async def connect_command(self, ctx: commands.Context, *, channel: nextcord.VoiceChannel = None):
        if channel:
            return await channel.connect(cls=wavelink.Player)
        elif ctx.author.voice is not None:
            return await ctx.author.voice.channel.connect(cls=wavelink.Player)
        else:
            not_connected = nextcord.Embed(title="Music",
                                           description=f"You aren't connected to a voice channel",
                                           color=ctx.author.color,
                                           timestamp=getter.get_time())
            return await ctx.send(embed=not_connected)

    @commands.command(name="disconnect", aliases=["leave"], help="Disconnect from a voice channel")
    async def disconnect_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if voice and voice.is_connected():
            disconnected = nextcord.Embed(title="Music",
                                          description=f"I have disconnected.",
                                          color=ctx.author.color,
                                          timestamp=getter.get_time())
            await voice.disconnect()
            return await ctx.send(embed=disconnected)
        not_connected = nextcord.Embed(title="Music",
                                       description=f"I am not to a voice channel.",
                                       color=ctx.author.color,
                                       timestamp=getter.get_time())
        await ctx.send(embed=not_connected)

    @commands.command(name="pause", help="Pause voice channel")
    async def pause_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if voice and voice.is_connected():
            if voice.is_paused():
                paused_already = nextcord.Embed(title="Music",
                                                description=f"I am already paused.",
                                                color=ctx.author.color,
                                                timestamp=getter.get_time())
                return await ctx.send(embed=paused_already)
            paused_already = nextcord.Embed(title="Music",
                                            description=f"The playback has been paused.",
                                            color=ctx.author.color,
                                            timestamp=getter.get_time())
            await voice.pause()
            return await ctx.send(embed=paused_already)
        not_connected = nextcord.Embed(title="Music",
                                       description=f"I am not to a voice channel.",
                                       color=ctx.author.color,
                                       timestamp=getter.get_time())
        await ctx.send(embed=not_connected)

    @commands.command(name="resume", help="Resume voice channel")
    async def resume_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if voice and voice.is_connected():
            if voice.is_paused():
                resumed = nextcord.Embed(title="Music",
                                         description=f"The playback has been resumed.",
                                         color=ctx.author.color,
                                         timestamp=getter.get_time())
                await voice.resume()
                return await ctx.send(embed=resumed)
            resumed = nextcord.Embed(title="Music",
                                     description=f"I am not paused.",
                                     color=ctx.author.color,
                                     timestamp=getter.get_time())
            return await ctx.send(embed=resumed)
        not_connected = nextcord.Embed(title="Music",
                                       description=f"I am not to a voice channel.",
                                       color=ctx.author.color,
                                       timestamp=getter.get_time())
        await ctx.send(embed=not_connected)

    @commands.command(name="stop", help="Stops the current song and clears the queue")
    async def stop_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if voice.is_playing():
            stopped = nextcord.Embed(title="Music",
                                     description=f"The playback has been stopped and the queue has been cleared.",
                                     color=ctx.author.color,
                                     timestamp=getter.get_time())
            voice.queue.clear()
            await voice.stop()
            return await ctx.send(embed=stopped)
        not_connected = nextcord.Embed(title="Music",
                                       description=f"I am not to a voice channel.",
                                       color=ctx.author.color,
                                       timestamp=getter.get_time())
        await ctx.send(embed=not_connected)

    @commands.command(name="volume", alias=["vol"], description="Change the volume of the player",
                      help="Change the volume of the player")
    async def volume_command(self, ctx: commands.Context, volume: int):
        voice: wavelink.Player = ctx.voice_client
        if not voice and not voice.is_connected():
            if volume < 0 or volume > 100:
                volume_must = nextcord.Embed(title="Music",
                                             description="Volume must be between 0 and 100",
                                             color=ctx.author.color,
                                             timestamp=getter.get_time())
                return await ctx.send(embed=volume_must)
            changed_volume = nextcord.Embed(title="Music",
                                            description=f"Changed volume to **{volume}**%",
                                            color=ctx.author.color,
                                            timestamp=getter.get_time())
            await voice.set_volume(volume)
            return await ctx.send(embed=changed_volume)
        not_connected = nextcord.Embed(title="Music",
                                       description=f"I am not to a voice channel.",
                                       color=ctx.author.color,
                                       timestamp=getter.get_time())
        await ctx.send(embed=not_connected)

    @commands.command(name="queue", help="Shows the current queue")
    async def queue_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client

        if not voice and not voice.is_connected():
            not_connected = nextcord.Embed(title="Music",
                                           description=f'No queue as we are not connected',
                                           color=ctx.author.color,
                                           timestamp=getter.get_time())
            return await ctx.send(embed=not_connected)
        queue_embed = nextcord.Embed(title="Music",
                                     description=f'No queue as we are not connected',
                                     color=ctx.author.color,
                                     timestamp=getter.get_time())
        queue_embed.add_field(name=f"Now Playing", value=f"{voice.queue.title}")
        queue_embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(voice.queue)

    @commands.command(name="Playing", aliases=["np"],
                      help="Shows the current song")
    async def playing_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client

        if not voice or not voice.is_connected():
            not_connected = nextcord.Embed(title="Music",
                                           description=f'I am not connected to a voice channel',
                                           color=ctx.author.color,
                                           timestamp=getter.get_time())
            return await ctx.send(embed=not_connected)
        queue_embed = nextcord.Embed(title="Music",
                                     description=f'No queue as we are not connected',
                                     color=ctx.author.color,
                                     timestamp=getter.get_time())
        queue_embed.add_field(name=f"Now Playing", value=f"{voice.track}")
        queue_embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(voice.queue)


def setup(bot):
    bot.add_cog(Music(bot))

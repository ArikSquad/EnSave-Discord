# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

import nextcord
import wavelink
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
        print(f'TRACK ENDED: {payload["reason"]}')

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: nextcord.Member,
                                    before: nextcord.VoiceState,
                                    after: nextcord.VoiceState):
        if member.id == self.bot.user.id:
            if before.channel is None and after.channel is not None:
                await member.edit(deafen=True)

    # noinspection PyTypeChecker
    @commands.command(name="play", description="Play a song.")
    async def play(self, ctx: commands.Context, *, query: str):
        voice: wavelink.Player = ctx.voice_client
        if not voice or not voice.is_connected():
            if ctx.author.voice is not None:
                voice: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
            else:
                not_connected = nextcord.Embed(title="Music",
                                               description=f"You aren't connected to a voice channel",
                                               color=ctx.author.color,
                                               timestamp=getter.get_time())
                return await ctx.send(embed=not_connected)

            track = await wavelink.YouTubeTrack.search(query=query, return_first=True)
            await voice.play(track)
            now_playing = nextcord.Embed(title="Music",
                                         description=f'**Now playing**: `{track.title}`',
                                         color=ctx.author.color,
                                         timestamp=getter.get_time())
            await ctx.send(embed=now_playing, delete_after=20)
        else:
            not_connected = nextcord.Embed(title="Music",
                                           description=f"You aren't connected to a voice channel",
                                           color=ctx.author.color,
                                           timestamp=getter.get_time())
            await ctx.send(embed=not_connected)

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
            await ctx.send(embed=disconnected)
            await voice.disconnect()
        else:
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
                await ctx.send(embed=paused_already)
            else:
                paused_already = nextcord.Embed(title="Music",
                                                description=f"The playback has been paused.",
                                                color=ctx.author.color,
                                                timestamp=getter.get_time())
                await ctx.send(embed=paused_already)
                await voice.pause()
        else:
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
                await ctx.send(embed=resumed)
                await voice.resume()
            else:
                resumed = nextcord.Embed(title="Music",
                                         description=f"I am not paused.",
                                         color=ctx.author.color,
                                         timestamp=getter.get_time())
                await ctx.send(embed=resumed)
        else:
            not_connected = nextcord.Embed(title="Music",
                                           description=f"I am not to a voice channel.",
                                           color=ctx.author.color,
                                           timestamp=getter.get_time())
            await ctx.send(embed=not_connected)

    @commands.command(name="volume", alias=["vol"], description="Change the volume of the player",
                      help="Change the volume of the player")
    async def volume_command(self, ctx: commands.Context, volume: int):
        voice: wavelink.Player = ctx.voice_client
        if voice and voice.is_connected():
            if volume < 0 or volume > 100:
                volume_must = nextcord.Embed(title="Music",
                                             description="Volume must be between 0 and 100",
                                             color=ctx.author.color,
                                             timestamp=getter.get_time())
                return await ctx.send(embed=volume_must)
            await voice.set_volume(volume)
            changed_volume = nextcord.Embed(title="Music",
                                            description=f"Changed volume to **{volume}**",
                                            color=ctx.author.color,
                                            timestamp=getter.get_time())
            await ctx.send(embed=changed_volume)
        else:
            not_connected = nextcord.Embed(title="Music",
                                           description=f"I am not to a voice channel.",
                                           color=ctx.author.color,
                                           timestamp=getter.get_time())
            await ctx.send(embed=not_connected)


def setup(bot):
    bot.add_cog(Music(bot))

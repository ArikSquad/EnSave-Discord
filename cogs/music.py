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

    # noinspection PyTypeChecker
    @commands.command(name="play", description="Play a song")
    async def play(self, ctx: commands.Context, *, query: str):
        voice: wavelink.Player = ctx.voice_client
        if not voice or not voice.is_connected():
            voice: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)

        track = await wavelink.YouTubeTrack.search(query=query, return_first=True)
        await voice.play(track)
        await ctx.send(f'**Now playing**: `{track.title}`', delete_after=20)
        await ctx.guild.change_voice_state(channel=ctx.voice_client.channel, self_deaf=True)

    # noinspection PyTypeChecker
    @commands.command(name="connect", aliases=["join"], help="Connect to a voice channel")
    async def connect_command(self, ctx: commands.Context, *, channel: nextcord.VoiceChannel = None):
        if channel:
            await ctx.guild.change_voice_state(channel=channel, self_deaf=True)
            return await channel.connect(cls=wavelink.Player)
        await ctx.guild.change_voice_state(channel=channel, self_deaf=True)
        return await ctx.author.voice.channel.connect(cls=wavelink.Player)

    # noinspection PyTypeChecker
    @commands.command(name="disconnect", aliases=["leave"], help="Disconnect from a voice channel")
    async def disconnect_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if voice and voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("no no no")

    # noinspection PyTypeChecker
    @commands.command(name="pause", help="Pause voice channel")
    async def pause_command(self, ctx: commands.Context):
        voice: wavelink.Player = ctx.voice_client
        if voice and voice.is_connected():
            await voice.pause()
        else:
            await ctx.send("no no no")


def setup(bot):
    bot.add_cog(Music(bot))

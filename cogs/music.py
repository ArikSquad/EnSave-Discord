# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2021 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# https://github.com/Carberra/discord.py-music-tutorial
# -----------------------------------------------------------

import asyncio
import datetime
import random
import re
import typing as t
from enum import Enum

import aiohttp
import discord
import requests
import validators
import wavelink
from discord.ext import commands

guild_ids = [770634445370687519]
URL_REGEX = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s(" \
            r")<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])) "
LYRICS_URL = "https://some-random-api.ml/lyrics?title="
HZ_BANDS = (20, 40, 63, 100, 150, 250, 400, 450, 630, 1000, 1600, 2500, 4000, 10000, 16000)
TIME_REGEX = r"([0-9]{1,2})[:ms](([0-9]{1,2})s?)?"
OPTIONS = {
    "1️⃣": 0,
    "2⃣": 1,
    "3⃣": 2,
    "4⃣": 3,
    "5⃣": 4,
}


def timestamp_embed():
    return datetime.datetime.now()


class AlreadyConnectedToChannel(commands.CommandError):
    pass


class NoVoiceChannel(commands.CommandError):
    pass


class QueueIsEmpty(commands.CommandError):
    pass


class NoTracksFound(commands.CommandError):
    pass


class PlayerIsAlreadyPaused(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class NoPreviousTracks(commands.CommandError):
    pass


class InvalidRepeatMode(commands.CommandError):
    pass


class VolumeTooLow(commands.CommandError):
    pass


class VolumeTooHigh(commands.CommandError):
    pass


class MaxVolume(commands.CommandError):
    pass


class MinVolume(commands.CommandError):
    pass


class NoLyricsFound(commands.CommandError):
    pass


class InvalidEQPreset(commands.CommandError):
    pass


class NonExistentEQBand(commands.CommandError):
    pass


class EQGainOutOfBounds(commands.CommandError):
    pass


class InvalidTimeString(commands.CommandError):
    pass


class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty

        self.position += 1

        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None

        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty

        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        if mode == "none":
            self.repeat_mode = RepeatMode.NONE
        elif mode == "1":
            self.repeat_mode = RepeatMode.ONE
        elif mode == "all":
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        self._queue.clear()
        self.position = 0


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()
        self.eq_levels = [0.] * 15

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel

        if (channel := getattr(ctx.author.voice, "channel", channel)) is None:
            raise NoVoiceChannel

        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        if not tracks:
            raise NoTracksFound

        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            embed1 = discord.Embed(
                description=f"Added {tracks[0].title} to the queue.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            embed1.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed1)
        else:
            if (track := await self.choose_track(ctx, tracks)) is not None:
                self.queue.add(track)
                embed2 = discord.Embed(
                    description=f"Added {track.title} to the queue.",
                    colour=ctx.author.colour,
                    timestamp=timestamp_embed()
                )
                embed2.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
                await ctx.send(embed=embed2)

        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                    r.emoji in OPTIONS.keys()
                    and u == ctx.author
                    and r.message.id == msg.id
            )

        embed = discord.Embed(
            title="Choose a song",
            description=(
                "\n".join(
                    f"**{i + 1}.** {typing.title} ({typing.length // 60000}:{str(typing.length % 60).zfill(2)})"
                    for i, typing in enumerate(tracks[:5])
                )
            ),
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Invoked by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        msg = await ctx.send(embed=embed)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)

        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.current_track)

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
        except QueueIsEmpty:
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)


class Music(commands.Cog, wavelink.WavelinkMixin, description="Music commands"):
    def __init__(self, bot):
        self.bot = bot
        self.bot.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild).teardown()

    @wavelink.WavelinkMixin.listener()
    async def on_node_ready(self, node):
        print(f" Wavelink node `{node.identifier}` ready.")

    @wavelink.WavelinkMixin.listener("on_track_stuck")
    @wavelink.WavelinkMixin.listener("on_track_end")
    @wavelink.WavelinkMixin.listener("on_track_exception")
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            embed = discord.Embed(
                description="Music commands are not available in DMs.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            await ctx.send(embed=embed)
            return False

        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = {
            "MAIN": {
                "host": "127.0.0.1",
                "port": 2333,
                "rest_uri": "http://localhost:2333",
                "password": "thisisarik",
                "identifier": "MAIN",
                "region": "europe",
            }
        }

        for node in nodes.values():
            await self.bot.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.bot.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.bot.wavelink.get_player(obj.id, cls=Player)

    @commands.command(name="connect", aliases=["join"], help="Connect to a voice channel")
    async def connect_command(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)
        embed = discord.Embed(
            description=f"Connected to {channel.name}.",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        await ctx.send(embed=embed)

    @connect_command.error
    async def connect_command_error(self, ctx, exc):
        if isinstance(exc, AlreadyConnectedToChannel):
            embed = discord.Embed(
                description="Already connected to a voice channel.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            await ctx.send(embed=embed)
        elif isinstance(exc, NoVoiceChannel):
            embed2 = discord.Embed(
                description="No suitable voice channel was provided.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            await ctx.send(embed=embed2)

    @commands.command(name="disconnect", aliases=["leave"], help="Disconnects from the voice channel.")
    async def disconnect_command(self, ctx):
        player = self.get_player(ctx)
        await player.teardown()
        embed = discord.Embed(
            description="Disconnected.",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        await ctx.send(embed=embed)

    @commands.command(name="weekly", aliases=["weeklysong", "daily", "featuredsong", "gamingsong", "featured"],
                      help="Play the weekly song.")
    async def weekly_command(self, ctx):
        player = self.get_player(ctx)

        if not player.is_connected:
            await player.connect(ctx)

        url = 'https://raw.githubusercontent.com/ArikSquad/EnSave-Discord/main/db/song.txt'
        page = requests.get(url)
        await player.add_tracks(ctx, await self.bot.wavelink.get_tracks(page.text))

    @commands.command(name="resume", aliases=["unpause"], help="Resume the player.")
    async def resume_command(self, ctx):
        player = self.get_player(ctx)
        await player.set_pause(False)
        embed = discord.Embed(
            description="Playback resumed.",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        await ctx.send(embed=embed)

    @commands.command(name="play", aliases=["yt", "youtube"], help="Play a song.")
    async def play_command(self, ctx, *, query: str):
        player = self.get_player(ctx)

        if validators.url(query) is True:
            embed3 = discord.Embed(
                description="We are sorry, but we don't support URLS.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            embed3.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed3)
        else:
            if not player.is_connected:
                await player.connect(ctx)

            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                query = f"ytsearch:{query}"

            await player.add_tracks(ctx, await self.bot.wavelink.get_tracks(query))

    @commands.command(name="soundcloud", aliases=["sc"], help="Play a song.")
    async def soundcloud_command(self, ctx, *, query: str):
        player = self.get_player(ctx)

        if validators.url(query) is True:
            embed3 = discord.Embed(
                description="We don't support URLS.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            embed3.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)

            await ctx.send(embed=embed3)
        else:
            if not player.is_connected:
                await player.connect(ctx)

            query = query.strip("<>")
            if not re.match(URL_REGEX, query):
                query = f"scsearch:{query}"

            await player.add_tracks(ctx, await self.bot.wavelink.get_tracks(query))

    @play_command.error
    async def play_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            embed = discord.Embed(
                description="No songs to play as the queue is empty.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            await ctx.send(embed=embed)
        elif isinstance(exc, NoVoiceChannel):
            embed2 = discord.Embed(
                description="No suitable voice channel was provided.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            await ctx.send(embed=embed2)

    @commands.command(name="pause", help="Pauses playback.")
    async def pause_command(self, ctx):
        player = self.get_player(ctx)

        if player.is_paused:
            raise PlayerIsAlreadyPaused

        await player.set_pause(True)
        embed = discord.Embed(
            description="Playback paused.",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @pause_command.error
    async def pause_command_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            embed = discord.Embed(
                description="Already paused.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(name="stop", help="Stops playback.")
    async def stop_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()
        embed = discord.Embed(
            description="Playback stopped.",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="next", aliases=["skip"], help="Skips to the next song.")
    async def next_command(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.upcoming:
            raise NoMoreTracks

        await player.stop()
        embed = discord.Embed(
            description="Playing next track in queue.",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        await ctx.send(embed=embed)

    @next_command.error
    async def next_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            embed = discord.Embed(
                description="This could not be executed as the queue is currently empty.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            await ctx.send(embed=embed)
        elif isinstance(exc, NoMoreTracks):
            embed2 = discord.Embed(
                description="There are no more tracks in the queue.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            await ctx.send(embed=embed2)

    @commands.command(name="previous", help="Plays the previous song.")
    async def previous_command(self, ctx):
        player = self.get_player(ctx)

        if not player.queue.history:
            raise NoPreviousTracks

        player.queue.position -= 2
        await player.stop()
        embed = discord.Embed(
            description="Playing previous track in queue.",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        await ctx.send(embed=embed)

    @previous_command.error
    async def previous_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            embed = discord.Embed(
                description="This could not be executed as the queue is currently empty.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            await ctx.send(embed=embed)
        elif isinstance(exc, NoPreviousTracks):
            embed2 = discord.Embed(
                description="There are no previous tracks in the queue.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            await ctx.send(embed=embed2)

    @commands.command(name="shuffle", help="Shuffles the queue.")
    async def shuffle_command(self, ctx):
        player = self.get_player(ctx)
        player.queue.shuffle()
        embed = discord.Embed(
            description="Queue shuffled.",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        await ctx.send(embed=embed)

    @shuffle_command.error
    async def shuffle_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            embed = discord.Embed(
                description="The queue could not be shuffled as it is currently empty.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            await ctx.send(embed=embed)

    @commands.command(name="repeat", aliases=["loop"], help="Repeats the songs.")
    async def repeat_command(self, ctx, mode: str):
        if mode not in ("none", "1", "all"):
            raise InvalidRepeatMode

        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)
        embed = discord.Embed(
            description=f"The repeat mode has been set to {mode}.",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        await ctx.send(embed=embed)

    @commands.command(name="queue", help="Shows the current queue.")
    async def queue_command(self, ctx, show: t.Optional[int] = 10):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = discord.Embed(
            title="Queue",
            description=f"Showing up to next {show} tracks",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        embed.set_author(name="Query Results")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        embed.add_field(
            name="Currently playing",
            value=getattr(player.queue.current_track, "title", "No tracks currently playing."),
            inline=False
        )
        if upcoming := player.queue.upcoming:
            embed.add_field(
                name="Next up",
                value="\n".join(typing.title for typing in upcoming[:show]),
                inline=False
            )

        await ctx.send(embed=embed)

    @queue_command.error
    async def queue_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            embed = discord.Embed(
                description="The queue is currently empty.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            await ctx.send(embed=embed)

    # Requests -----------------------------------------------------------------

    @commands.group(name="volume", aliases=["vol"], invoke_without_command=True, help="Adjusts the volume.")
    async def volume_group(self, ctx, volume: int):
        player = self.get_player(ctx)

        if volume < 0:
            raise VolumeTooLow

        if volume > 150:
            raise VolumeTooHigh

        await player.set_volume(volume)
        embed = discord.Embed(
            description=f"Volume set to {volume:,}%",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        await ctx.send(embed=embed)

    @volume_group.error
    async def volume_group_error(self, ctx, exc):
        if isinstance(exc, VolumeTooLow):
            embed = discord.Embed(
                description="The volume must be 0% or above.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            await ctx.send(embed=embed)
        elif isinstance(exc, VolumeTooHigh):
            embed2 = discord.Embed(
                description="The volume must be 150% or below.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            await ctx.send(embed=embed2)

    @volume_group.command(name="up")
    async def volume_up_command(self, ctx):
        player = self.get_player(ctx)

        if player.volume == 150:
            raise MaxVolume

        await player.set_volume(value := min(player.volume + 10, 150))
        embed = discord.Embed(
            description=f"Volume set to {value:,}%",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        await ctx.send(embed=embed)

    @volume_up_command.error
    async def volume_up_command_error(self, ctx, exc):
        if isinstance(exc, MaxVolume):
            embed = discord.Embed(
                description="The player is already at max volume.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            await ctx.send(embed=embed)

    @volume_group.command(name="down")
    async def volume_down_command(self, ctx):
        player = self.get_player(ctx)

        if player.volume == 0:
            raise MinVolume

        await player.set_volume(value := max(0, player.volume - 10))
        embed = discord.Embed(
            description=f"Volume set to {value:,}%",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        await ctx.send(embed=embed)

    @volume_down_command.error
    async def volume_down_command_error(self, ctx, exc):
        if isinstance(exc, MinVolume):
            embed = discord.Embed(
                description="The player is already at min volume.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            await ctx.send(embed=embed)

    @commands.command(name="lyrics", help="Gets the lyrics of the current track.")
    async def lyrics_command(self, ctx, name: t.Optional[str]):
        player = self.get_player(ctx)
        name = name or player.queue.current_track.title

        async with ctx.typing():
            async with aiohttp.request("GET", LYRICS_URL + name, headers={}) as r:
                if not 200 <= r.status <= 299:
                    raise NoLyricsFound

                data = await r.json()

                if len(data["lyrics"]) > 2000:
                    embed2 = discord.Embed(
                        title=data["title"],
                        description=f"<{data['links']['genius']}>",
                        colour=ctx.author.colour,
                        timestamp=timestamp_embed()
                    )
                    embed2.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
                    return await ctx.send(embed=embed2)

                embed = discord.Embed(
                    title=data["title"],
                    description=data["lyrics"],
                    colour=ctx.author.colour,
                    timestamp=timestamp_embed()
                )
                embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
                embed.set_thumbnail(url=data["thumbnail"]["genius"])
                embed.set_author(name=data["author"])
                await ctx.send(embed=embed)

    @lyrics_command.error
    async def lyrics_command_error(self, ctx, exc):
        if isinstance(exc, NoLyricsFound):
            embed2 = discord.Embed(
                description="No lyrics could be found.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            embed2.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed2)

    @commands.command(name="eq", aliases=["equaliser"], help="Adjust the EQ settings.", )
    async def eq_command(self, ctx, preset: str):
        player = self.get_player(ctx)

        eq = getattr(wavelink.eqs.Equalizer, preset, None)
        if not eq:
            raise InvalidEQPreset

        await player.set_eq(eq())
        embed2 = discord.Embed(
            description=f"Equaliser adjusted to the {preset} preset.",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        await ctx.send(embed=embed2)

    @eq_command.error
    async def eq_command_error(self, ctx, exc):
        if isinstance(exc, InvalidEQPreset):
            embed = discord.Embed(
                description="The EQ preset must be either 'flat', 'boost', 'metal', or 'piano'.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            await ctx.send(embed=embed)

    @commands.command(name="adveq", aliases=["aeq"], help="Adjust the advanced EQ settings.", )
    async def adveq_command(self, ctx, band: int, gain: float):
        player = self.get_player(ctx)

        if not 1 <= band <= 15 and band not in HZ_BANDS:
            raise NonExistentEQBand

        if band > 15:
            band = HZ_BANDS.index(band) + 1

        if abs(gain) > 10:
            raise EQGainOutOfBounds

        player.eq_levels[band - 1] = gain / 10
        eq = wavelink.eqs.Equalizer(levels=[(i, gain) for i, gain in enumerate(player.eq_levels)])
        await player.set_eq(eq)
        embed2 = discord.Embed(
            description="Equaliser adjusted.",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        await ctx.send(embed=embed2)

    @adveq_command.error
    async def adveq_command_error(self, ctx, exc):
        embed = discord.Embed(
            description="This is a 15 band equaliser "
                        "-- the band number should be between 1 and 15, or one of the following "
                        "frequencies: " + ", ".join(str(b) for b in HZ_BANDS),
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        embed2 = discord.Embed(
            description="The EQ gain for any band should be between 10 dB and -10 dB.",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        if isinstance(exc, NonExistentEQBand):

            await ctx.send(embed=embed)
        elif isinstance(exc, EQGainOutOfBounds):
            await ctx.send(embed=embed2)

    @commands.command(name="playing", aliases=["np", "info", "musicinfo"],
                      help="Get information about the current song.", )
    async def playing_command(self, ctx):
        player = self.get_player(ctx)

        if not player.is_playing:
            raise PlayerIsAlreadyPaused

        embed = discord.Embed(
            title="Now playing",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        embed.set_author(name="Playback Information")
        embed.set_footer(text=f"Requested by {ctx.author.display_name}", icon_url=ctx.author.avatar_url)
        if str(player.current.identifier).startswith("O:https://api-v2.soundcloud.com"):
            embed.add_field(name="Track title",
                            value=player.queue.current_track.title,
                            inline=False)
        else:
            embed.add_field(name="Track title",
                            value=f"[{player.queue.current_track.title}]"
                                  f"(https://youtube.com/watch?v={player.current.identifier})",
                            inline=False)
        embed.add_field(name="Artist", value=player.queue.current_track.author, inline=False)

        position = divmod(player.position, 60000)
        length = divmod(player.queue.current_track.length, 60000)
        embed.add_field(
            name="Position",
            value=f"{int(position[0])}:{round(position[1] / 1000):02}/{int(length[0])}:{round(length[1] / 1000):02}",
            inline=False
        )

        await ctx.send(embed=embed)

    @playing_command.error
    async def playing_command_error(self, ctx, exc):
        embed = discord.Embed(
            description="There is no track currently playing.",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send(embed=embed)

    @commands.command(name="skipto", aliases=["playindex"], help="Skip to a specific track in the queue.", )
    async def skipto_command(self, ctx, index: int):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        if not 0 <= index <= player.queue.length:
            raise NoMoreTracks

        player.queue.position = index - 2
        await player.stop()
        embed = discord.Embed(
            description=f"Playing track in position {index}.",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        await ctx.send(embed=embed)

    @skipto_command.error
    async def skipto_command_error(self, ctx, exc):
        embed = discord.Embed(
            description="There are no tracks in the queue.",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        embed2 = discord.Embed(
            description="That index is out of the bounds of the queue.",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        if isinstance(exc, QueueIsEmpty):
            await ctx.send(embed=embed)
        elif isinstance(exc, NoMoreTracks):
            await ctx.send(embed=embed2)

    @commands.command(name="restart", help="Restart the current track.", )
    async def restart_command(self, ctx):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        await player.seek(0)
        embed = discord.Embed(
            description="Track restarted.",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        await ctx.send(embed=embed)

    @restart_command.error
    async def restart_command_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            embed = discord.Embed(
                description="There are no tracks in the queue.",
                colour=ctx.author.colour,
                timestamp=timestamp_embed()
            )
            await ctx.send(embed=embed)

    @commands.command(name="seek", help="Seek to a specific time in the current track.", )
    async def seek_command(self, ctx, position: str):
        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        if not (match := re.match(TIME_REGEX, position)):
            raise InvalidTimeString

        if match.group(3):
            secs = (int(match.group(1)) * 60) + (int(match.group(3)))
        else:
            secs = int(match.group(1))

        await player.seek(secs * 1000)
        embed = discord.Embed(
            description="Seeked",
            colour=ctx.author.colour,
            timestamp=timestamp_embed()
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Music(bot))

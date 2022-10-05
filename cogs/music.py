# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import datetime
import json
import os
import typing

import discord
import requests
import wavelink
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
host_server = str(os.getenv('MUSIC'))
host_pass = str(os.getenv('MUSIC_PASSWORD'))


class Player:
    @staticmethod
    async def skip(interaction: discord.Interaction, voice: wavelink.Player):
        if interaction.user.voice:
            if interaction.user.voice.channel is voice.channel:
                if not voice.queue.is_empty:
                    await voice.stop()
                    skipped = discord.Embed(title="Queue",
                                            description=f"The song has been skipped and now playing {voice.queue[0]}",
                                            color=discord.Color.from_rgb(48, 50, 54),
                                            timestamp=datetime.datetime.utcnow())
                    return await interaction.response.send_message(embed=skipped)
                else:
                    not_connected = discord.Embed(title="Queue",
                                                  description=f"Play some songs first.",
                                                  color=discord.Color.from_rgb(48, 50, 54),
                                                  timestamp=datetime.datetime.utcnow())
                    await interaction.response.send_message(embed=not_connected, ephemeral=True)
            else:
                not_same = discord.Embed(title="Music",
                                         description=f"We aren't in the same channel.",
                                         color=discord.Color.from_rgb(48, 50, 54),
                                         timestamp=datetime.datetime.utcnow())
                await interaction.response.send_message(embed=not_same, ephemeral=True)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"We are not connected to the voice channel.",
                                          color=discord.Color.from_rgb(48, 50, 54),
                                          timestamp=datetime.datetime.utcnow())
            return await interaction.response.send_message(embed=not_connected, ephemeral=True)

    @staticmethod
    async def pause(interaction: discord.Interaction, voice: wavelink.Player):
        if interaction.user.voice:
            if voice and voice.is_connected():
                if voice.is_paused():
                    paused_already = discord.Embed(title="Queue",
                                                   description=f"I am already paused.",
                                                   color=discord.Color.from_rgb(48, 50, 54),
                                                   timestamp=datetime.datetime.utcnow())
                    return await interaction.response.send_message(embed=paused_already, ephemeral=True)
                if voice.channel is interaction.user.voice.channel:
                    paused = discord.Embed(title="Queue",
                                           description=f"The playback has been paused.",
                                           color=discord.Color.from_rgb(48, 50, 54),
                                           timestamp=datetime.datetime.utcnow())
                    await voice.pause()
                    return await interaction.response.send_message(embed=paused)
                else:
                    not_same = discord.Embed(title="Queue",
                                             description=f"We aren't in the same channel.",
                                             color=discord.Color.from_rgb(48, 50, 54),
                                             timestamp=datetime.datetime.utcnow())
                    return await interaction.response.send_message(embed=not_same, ephemeral=True)
            else:
                not_connected = discord.Embed(title="Music",
                                              description=f"I am not in a voice channel.",
                                              color=discord.Color.from_rgb(48, 50, 54),
                                              timestamp=datetime.datetime.utcnow())
                await interaction.response.send_message(embed=not_connected, ephemeral=True)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"You are not connected to the voice channel.",
                                          color=discord.Color.from_rgb(48, 50, 54),
                                          timestamp=datetime.datetime.utcnow())
            return await interaction.response.send_message(embed=not_connected, ephemeral=True)

    @staticmethod
    async def resume(interaction: discord.Interaction, voice: wavelink.Player):
        if interaction.user.voice:
            if voice and voice.is_connected():
                if voice.is_paused() and voice.channel is interaction.user.voice.channel:
                    resumed = discord.Embed(title="Queue",
                                            description=f"The playback has been resumed.",
                                            color=discord.Color.from_rgb(48, 50, 54),
                                            timestamp=datetime.datetime.utcnow())
                    await voice.resume()
                    await interaction.response.send_message(embed=resumed)
                else:
                    resumed = discord.Embed(title="Queue",
                                            description=f"I am not paused.",
                                            color=discord.Color.from_rgb(48, 50, 54),
                                            timestamp=datetime.datetime.utcnow())
                    await interaction.response.send_message(embed=resumed, ephemeral=True)
            else:
                not_connected = discord.Embed(title="Music",
                                              description=f"I am not in a voice channel.",
                                              color=discord.Color.from_rgb(48, 50, 54),
                                              timestamp=datetime.datetime.utcnow())
                await interaction.response.send_message(embed=not_connected, ephemeral=True)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"You are not connected to the voice channel.",
                                          color=discord.Color.from_rgb(48, 50, 54),
                                          timestamp=datetime.datetime.utcnow())
            return await interaction.response.send_message(embed=not_connected, ephemeral=True)

    @staticmethod
    async def stop(interaction: discord.Interaction, voice: wavelink.Player):
        if interaction.user.voice and voice:
            if voice.is_playing() | voice.is_paused():
                if voice.channel is interaction.user.voice.channel:
                    stopped = discord.Embed(title="Queue",
                                            description=f"The playback has been stopped "
                                                        f"and the queue has been cleared.",
                                            color=discord.Color.from_rgb(48, 50, 54),
                                            timestamp=datetime.datetime.utcnow())

                    # This will clear the queue and stop the player
                    voice.queue.clear()
                    await voice.stop()

                    await interaction.response.send_message(embed=stopped)
                else:
                    not_same = discord.Embed(title="Queue",
                                             description=f"We aren't in the same channel.",
                                             color=discord.Color.from_rgb(48, 50, 54),
                                             timestamp=datetime.datetime.utcnow())
                    await interaction.response.send_message(embed=not_same, ephemeral=True)
            else:
                not_connected = discord.Embed(title="Queue",
                                              description=f"Music isn't playing.",
                                              color=discord.Color.from_rgb(48, 50, 54),
                                              timestamp=datetime.datetime.utcnow())
                await interaction.response.send_message(embed=not_connected, ephemeral=True)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"We are not connected to the voice channel.",
                                          color=discord.Color.from_rgb(48, 50, 54),
                                          timestamp=datetime.datetime.utcnow())
            return await interaction.response.send_message(embed=not_connected, ephemeral=True)


# noinspection PyUnusedLocal
class PlayerView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=30)
        self.back_button.disabled = True
        self.message = None

    async def on_timeout(self) -> None:
        for item in self.children:
            item.disabled = True
        await self.message.edit(view=self)

    @discord.ui.button(label='⬅', style=discord.ButtonStyle.gray)
    async def back_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()

    @discord.ui.button(label='▶', style=discord.ButtonStyle.blurple)
    async def resume_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice: wavelink.Player = interaction.guild.voice_client
        await Player.resume(interaction, voice)

    @discord.ui.button(label='🟥', style=discord.ButtonStyle.red)
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice: wavelink.Player = interaction.guild.voice_client
        await Player.stop(interaction, voice)

    @discord.ui.button(label='⏸', style=discord.ButtonStyle.blurple)
    async def pause_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice: wavelink.Player = interaction.guild.voice_client
        await Player.pause(interaction, voice)

    @discord.ui.button(label='➡', style=discord.ButtonStyle.green)
    async def skip_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        voice: wavelink.Player = interaction.guild.voice_client
        await Player.skip(interaction, voice)


# noinspection PyTypeChecker
class Music(commands.Cog, description="Play songs in voice channels"):
    group = app_commands.Group(name='music', description='Play some songs and rickroll your friends')

    def __init__(self, bot):
        self.bot = bot
        self.node: wavelink.Node = None

    # Create connect node task, when the bot is ready
    @commands.Cog.listener()
    async def on_ready(self) -> None:
        self.bot.loop.create_task(self.connect_nodes())

    # Connect the bot to a lavalink server
    async def connect_nodes(self) -> None:
        node = await wavelink.NodePool.create_node(bot=self.bot, host=host_server, port=2333, password=host_pass)
        self.node = node

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

    # noinspection PyUnusedLocal
    async def play_autocomplete(self, interaction: discord.Interaction,
                                current: str) -> typing.List[app_commands.Choice[str]]:
        search = await self.node.get_tracks(cls=wavelink.YouTubeTrack, query=f"ytsearch:{current}")
        return [
            app_commands.Choice(name=track.title, value=track.title)
            for track in search if current.lower() in track.title.lower()
        ]

    # Command to play songs in a voice channel
    @group.command(name="play", description="Play a song.")
    @app_commands.autocomplete(query=play_autocomplete)
    @app_commands.describe(query='Song that you want to play')
    async def play(self, interaction: discord.Interaction, query: str) -> None:
        await interaction.response.defer()
        # This will soon change when we find a way to use spotify
        song: wavelink.YouTubeTrack = (await self.node.get_tracks(cls=wavelink.YouTubeTrack,
                                                                  query=f"ytsearch:{query}"))[0]
        if not interaction.user.voice:
            not_connected = discord.Embed(title="Music",
                                          description=f"You are not connected to a voice channel.",
                                          color=discord.Color.from_rgb(48, 50, 54),
                                          timestamp=datetime.datetime.utcnow())
            return await interaction.user.send(embed=not_connected)

        voice: wavelink.Player = interaction.guild.voice_client or await \
            interaction.user.voice.channel.connect(cls=wavelink.Player)

        if voice.queue.is_empty and not voice.is_playing():
            view = PlayerView()
            now_playing = discord.Embed(title="Queue",
                                        description=f'**Now playing**: [{song.title}]'
                                                    f'({song.uri})',
                                        color=discord.Color.from_rgb(48, 50, 54),
                                        timestamp=datetime.datetime.utcnow())
            now_playing.add_field(name="Author", value=f"{song.author}")
            now_playing.set_thumbnail(url=song.thumbnail)
            await voice.play(song)
            await interaction.followup.send(embed=now_playing, view=view)
            view.message = await interaction.original_response()
            return

        added_queue = discord.Embed(title="Queue",
                                    description=f"Added [{song.title}]"
                                                f"({song.uri}) to the queue.",
                                    color=discord.Color.from_rgb(48, 50, 54),
                                    timestamp=datetime.datetime.utcnow())
        added_queue.set_thumbnail(url=song.thumbnail)
        added_queue.add_field(name="Author", value=f"{song.author}")

        await voice.queue.put_wait(song)
        await interaction.followup.send(embed=added_queue)

    # Command for connecting to a voice channel. You can specify the channel or not, so it joins the channel you are in
    @group.command(name="connect", description="Connect to a voice channel")
    @app_commands.describe(channel='The channel to connect to')
    async def connect_command(self, interaction: discord.Interaction, channel: discord.VoiceChannel = None) -> None:
        voice: wavelink.Player = interaction.guild.voice_client
        if channel:
            if voice.channel != channel:
                await voice.move_to(channel)
            else:
                await channel.connect(cls=wavelink.Player)
            connected_success = discord.Embed(title="Music",
                                              description=f"Connected to `{channel.name}`",
                                              color=discord.Color.from_rgb(48, 50, 54),
                                              timestamp=datetime.datetime.utcnow())

            return await interaction.response.send_message(embed=connected_success)
        else:
            if interaction.user.voice:
                if voice.channel != interaction.user.voice.channel:
                    await voice.move_to(interaction.user.voice.channel)
                else:
                    await interaction.user.voice.channel.connect(cls=wavelink.Player)
                connected_success = discord.Embed(title="Music",
                                                  description=f"Connected to `{interaction.user.voice.channel.name}`",
                                                  color=discord.Color.from_rgb(48, 50, 54),
                                                  timestamp=datetime.datetime.utcnow())
                await interaction.response.send_message(embed=connected_success)
            else:
                not_connected = discord.Embed(title="Music",
                                              description=f"You are not connected to a voice channel.",
                                              color=discord.Color.from_rgb(48, 50, 54),
                                              timestamp=datetime.datetime.utcnow())
                return await interaction.response.send_message(embed=not_connected, ephemeral=True)

    # Command to leave from a voice channel
    @group.command(name="disconnect", description="Disconnect from a voice channel")
    async def disconnect_command(self, interaction: discord.Interaction) -> None:
        voice: wavelink.Player = interaction.guild.voice_client
        if interaction.user.voice:
            if voice and voice.is_connected():
                if voice.channel is interaction.user.voice.channel:
                    disconnected = discord.Embed(title='Music',
                                                 description=f'I have disconnected from '
                                                             f'`{voice.channel.name}`.',
                                                 color=discord.Color.from_rgb(48, 50, 54),
                                                 timestamp=datetime.datetime.utcnow())
                    await voice.disconnect()
                    return await interaction.response.send_message(embed=disconnected)
                else:
                    not_connected = discord.Embed(title="Music",
                                                  description=f"You aren't in the same voice channel as I am.",
                                                  color=discord.Color.from_rgb(48, 50, 54),
                                                  timestamp=datetime.datetime.utcnow())
                    return await interaction.response.send_message(embed=not_connected, ephemeral=True)
            else:
                not_connected = discord.Embed(title='Music',
                                              description=f"I am not in a voice channel.",
                                              color=discord.Color.from_rgb(48, 50, 54),
                                              timestamp=datetime.datetime.utcnow())
                await interaction.response.send_message(embed=not_connected, ephemeral=True)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"You are not connected to the voice channel.",
                                          color=discord.Color.from_rgb(48, 50, 54),
                                          timestamp=datetime.datetime.utcnow())
            return await interaction.response.send_message(embed=not_connected, ephemeral=True)

    # Command for pausing your songs
    @group.command(name="pause", description="Pause the current song")
    async def pause_command(self, interaction: discord.Interaction) -> None:
        voice: wavelink.Player = interaction.guild.voice_client
        await Player.pause(interaction, voice)

    # Command to resume listening to your songs
    @group.command(name="resume", description="Resume song that was playing before")
    async def resume_command(self, interaction: discord.Interaction) -> None:
        voice: wavelink.Player = interaction.guild.voice_client
        await Player.resume(interaction, voice)

    # Command to stop the music and clear the queue
    @group.command(name="stop", description="Stops the current song and clears the queue")
    async def stop_command(self, interaction: discord.Interaction) -> None:
        voice: wavelink.Player = interaction.guild.voice_client
        await Player.stop(interaction, voice)

    # Command to change the volume of the player
    @group.command(name="volume", description="Change the volume of the player")
    @app_commands.describe(volume='The volume of the song')
    async def volume_command(self, interaction: discord.Interaction, volume: app_commands.Range[int, 0, 100]):
        voice: wavelink.Player = interaction.guild.voice_client
        if interaction.user.voice:
            if voice and voice.is_connected():
                if voice.channel is interaction.user.voice.channel:
                    changed_volume = discord.Embed(title="Music",
                                                   description=f"Changed volume to **{volume}**%",
                                                   color=discord.Color.from_rgb(48, 50, 54),
                                                   timestamp=datetime.datetime.utcnow())
                    await voice.set_volume(volume)
                    await interaction.response.send_message(embed=changed_volume)
                else:
                    not_same = discord.Embed(title="Music",
                                             description=f"We aren't in the same channel.",
                                             color=discord.Color.from_rgb(48, 50, 54),
                                             timestamp=datetime.datetime.utcnow())
                    await interaction.response.send_message(embed=not_same, ephemeral=True)
            else:
                not_connected = discord.Embed(title="Queue",
                                              description=f"I am not in a voice channel.",
                                              color=discord.Color.from_rgb(48, 50, 54),
                                              timestamp=datetime.datetime.utcnow())
                await interaction.response.send_message(embed=not_connected, ephemeral=True)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"You are not connected to the voice channel.",
                                          color=discord.Color.from_rgb(48, 50, 54),
                                          timestamp=datetime.datetime.utcnow())
            return await interaction.response.send_message(embed=not_connected, ephemeral=True)

    # Command to shuffle the order of tracks. This command is limited to premium users
    @group.command(name="shuffle", description="Shuffle the queue.")
    async def shuffle_command(self, interaction: discord.Interaction):
        voice: wavelink.Player = interaction.guild.voice_client
        if interaction.user.voice and voice:
            if not voice.is_playing():
                not_connected = discord.Embed(title="Queue",
                                              description="Music isn't playing.",
                                              color=discord.Color.from_rgb(48, 50, 54),
                                              timestamp=datetime.datetime.utcnow())
                return await interaction.response.send_message(embed=not_connected, ephemeral=True)
            if not voice.queue():
                no_tracks = discord.Embed(title="Queue",
                                          description=f"No tracks are queued.",
                                          color=discord.Color.from_rgb(48, 50, 54),
                                          timestamp=datetime.datetime.utcnow())
                return await interaction.response.send_message(embed=no_tracks, ephemeral=True)
            voice.queue.shuffle()
            shuffle = discord.Embed(title="Queue",
                                    description=f"Shuffled the queue",
                                    color=discord.Color.from_rgb(48, 50, 54),
                                    timestamp=datetime.datetime.utcnow())
            await interaction.response.send_message(embed=shuffle)
        else:
            not_connected = discord.Embed(title="Music",
                                          description=f"You are not connected to the voice channel.",
                                          color=discord.Color.from_rgb(48, 50, 54),
                                          timestamp=datetime.datetime.utcnow())
            return await interaction.response.send_message(embed=not_connected, ephemeral=True)

    # Command to see information about the current track.
    @group.command(name="playing", description="Gives more information about the current track.")
    async def playing_command(self, interaction: discord.Interaction):
        voice: wavelink.Player = interaction.guild.voice_client
        if voice.queue:
            song = await voice.queue.get()
            embed = discord.Embed(title="Queue",
                                  description=f"**{song.title}**\n\n"
                                  )
            if isinstance(song, wavelink.YouTubeTrack):
                embed.set_thumbnail(url=song.thumbnail)
            embed.add_field(name="Author", value=song.author)
            await interaction.response.send_message(embed=embed)
        else:
            no_tracks = discord.Embed(title="Queue",
                                      description=f"No tracks are queued.",
                                      color=discord.Color.from_rgb(48, 50, 54),
                                      timestamp=datetime.datetime.utcnow())
            await interaction.response.send_message(embed=no_tracks, ephemeral=True)

    # Command to skip songs
    @group.command(name="skip", description="Skips the current song.")
    async def skip_command(self, interaction: discord.Interaction):
        voice: wavelink.Player = interaction.guild.voice_client
        await Player.skip(interaction, voice)

    @group.command(name="lyrics", description="Gets the lyrics of the current track.")
    @app_commands.describe(name='The name of the song')
    async def lyrics_command(self, interaction: discord.Interaction, name: str = None):
        await interaction.response.defer()
        voice: wavelink.Player = interaction.guild.voice_client
        if not name:
            if voice.is_playing():
                name = voice.source.title
            else:
                name = "Never Gonna Give You Up"

        response = requests.get("https://some-random-api.ml/lyrics?title=" + name)
        if response.status_code == 200:
            data = json.loads(response.content)
        else:
            return await interaction.followup.send("Could not found anything.")
        if data.get("lyrics"):
            if len(data.get("lyrics")) > 2000:
                embed2 = discord.Embed(
                    title=data.get("title"),
                    description=f"<{data['links']['genius']}>",
                    colour=interaction.user.colour,
                    timestamp=datetime.datetime.utcnow())
                return await interaction.followup.send(embed=embed2)

            embed = discord.Embed(
                title=data["title"],
                description=data["lyrics"],
                colour=interaction.user.colour,
                timestamp=datetime.datetime.utcnow())
            embed.set_thumbnail(url=data["thumbnail"]["genius"])
            embed.set_author(name=data["author"])
            await interaction.followup.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Music(bot))

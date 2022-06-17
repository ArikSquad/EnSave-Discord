# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# This file is for the buttons, and it doesn't need comments
# -----------------------------------------------------------
import datetime

import discord
from discord import Interaction


# noinspection PyUnusedLocal
class Resume(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    async def on_timeout(self) -> None:
        self.clear_items()

    @discord.ui.button(label="Resume", style=discord.ButtonStyle.blurple)
    async def _resume(self, interaction: Interaction, button: discord.ui.Button) -> None:
        paused = discord.Embed(title="Music",
                               description=f"The playback has been resumed.",
                               color=interaction.user.color,
                               timestamp=datetime.datetime.utcnow())
        await interaction.response.send_message(embed=paused)
        self.value = True
        self.stop()


# noinspection PyUnusedLocal
class YesNo(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    async def on_timeout(self) -> None:
        self.clear_items()

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.danger)
    async def _yes(self, interaction: Interaction, button: discord.ui.Button) -> None:
        self.value = True
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.green)
    async def _no(self, interaction: Interaction, button: discord.ui.Button) -> None:
        await interaction.response.send_message(f"Okay, we won't do that then!", ephemeral=True)
        self.value = False
        self.stop()

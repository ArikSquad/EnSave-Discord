# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

import discord
from discord import Interaction

from utils.database import get_time


# noinspection PyUnusedLocal
class Resume(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    async def on_timeout(self):
        self.clear_items()

    @discord.ui.button(label="Resume", style=discord.ButtonStyle.blurple)
    async def _resume(self, interaction: Interaction, button: discord.ui.Button):
        paused = discord.Embed(title="Music",
                               description=f"The playback has been resumed.",
                               color=interaction.user.color,
                               timestamp=get_time())
        await interaction.response.send_message(embed=paused)
        self.value = True
        self.stop()


# noinspection PyUnusedLocal
class YesNo(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    async def on_timeout(self):
        self.clear_items()

    @discord.ui.button(label="Yes", style=discord.ButtonStyle.danger)
    async def _yes(self, interaction: Interaction, button: discord.ui.Button):
        self.value = True
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.green)
    async def _no(self, interaction: Interaction, button: discord.ui.Button):
        await interaction.response.send_message(f"Okay, we won't do that then!", ephemeral=True)
        self.value = False
        self.stop()

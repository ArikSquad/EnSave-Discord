# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

import datetime
import json

import nextcord
from nextcord import Interaction


def get_time():
    return datetime.datetime.utcnow()


def get_guild_ids():
    return [770634445370687519]


def get_owner_id():
    return 549152470194978817


def get_premium(user_id):
    try:
        with open('db/premium.json', 'r') as f:
            data = json.load(f)
        if data[str(user_id)] == "true":
            return True
        else:
            return False
    except KeyError:
        with open('db/premium.json', 'w') as f:
            data[str(user_id)] = "false"
            json.dump(data, f, indent=4)
        return False


def premium_embed(ctx, title: str):
    return nextcord.Embed(title=title,
                          description="You need to be a premium user to use this command.",
                          color=ctx.author.color,
                          timestamp=get_time())


# noinspection PyUnusedLocal
class PauseStop(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="Pause", style=nextcord.ButtonStyle.blurple)
    async def _pause(self, button: nextcord.ui.Button, interaction: Interaction):
        paused = nextcord.Embed(title="Music",
                                description=f"The playback has been paused.",
                                color=interaction.user.color,
                                timestamp=get_time())
        await interaction.send(embed=paused)
        self.value = "pause"
        self.stop()

    @nextcord.ui.button(label="Stop", style=nextcord.ButtonStyle.danger)
    async def _stop(self, button: nextcord.ui.Button, interaction: Interaction):
        stopped = nextcord.Embed(title="Music",
                                 description=f"The playback has been stopped.",
                                 color=interaction.user.color,
                                 timestamp=get_time())
        await interaction.send(embed=stopped)
        self.value = "stop"
        self.stop()


class Resume(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="Resume", style=nextcord.ButtonStyle.blurple)
    async def _resume(self, button: nextcord.ui.Button, interaction: Interaction):
        paused = nextcord.Embed(title="Music",
                                description=f"The playback has been resumed.",
                                color=interaction.user.color,
                                timestamp=get_time())
        await interaction.send(embed=paused)
        self.value = True
        self.stop()


# noinspection PyUnusedLocal
class YesNo(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(label="Yes", style=nextcord.ButtonStyle.danger)
    async def _yes(self, button: nextcord.ui.Button, interaction: Interaction):
        self.value = True
        self.stop()

    @nextcord.ui.button(label="No", style=nextcord.ButtonStyle.green)
    async def _no(self, button: nextcord.ui.Button, interaction: Interaction):
        await interaction.send(f"Okay, we won't do that then!", ephemeral=True)
        self.value = False
        self.stop()


# noinspection PyUnusedLocal
class Cookie(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @nextcord.ui.button(emoji="🍪", style=nextcord.ButtonStyle.blurple)
    async def _cookie(self, button: nextcord.ui.Button, interaction: Interaction):
        embed = nextcord.Embed(title="Cookie",
                               description=f"{interaction.user.mention} have received a cookie.",
                               color=interaction.user.color,
                               timestamp=get_time())
        self.value = True
        self.stop()

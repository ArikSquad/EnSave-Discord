# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

import datetime
import json

import discord
from discord import Interaction


def get_time():
    return datetime.datetime.utcnow()


def get_guild_ids():
    return [770634445370687519]


def get_owners_discord():
    return ["ArikSquad#6222", "Mhilkos#7676"]


def get_owner_ids():
    return [549152470194978817]


def get_prefix(ctx, message):
    with open('db/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    if str(message.guild.id) in prefixes:
        return prefixes[str(message.guild.id)]
    else:
        prefixes[str(message.guild.id)] = '.'
        with open('db/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        return prefixes[str(message.guild.id)]


def get_prefix_by_id(guild_id):
    with open('db/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    if str(guild_id) in prefixes:
        return prefixes[str(guild_id)]
    else:
        prefixes[str(guild_id)] = '.'
        with open('db/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
        return prefixes[str(guild_id)]


def set_prefix(guild_id, prefix):
    with open('db/prefixes.json', 'r+') as f:
        data = json.load(f)
    data[str(guild_id)] = prefix
    with open('db/prefixes.json', 'w') as f:
        json.dump(data, f, indent=4)


def get_premium(user_id):
    with open('db/users.json', 'r') as f:
        data = json.load(f)

    if user_id in data:
        if data[str(user_id)]['premium']:
            return True
        else:
            with open('db/users.json', 'w') as f:
                data[str(user_id)]['premium'] = False
                json.dump(data, f, indent=4, sort_keys=True)
            return False
    else:
        with open('db/users.json', 'w') as f:
            data[str(user_id)]['premium'] = False
            json.dump(data, f, indent=4, sort_keys=True)
        return False


def set_premium(user_id, premium: bool = True):
    with open('db/users.json', 'r+') as f:
        data = json.load(f)
        data[str(user_id)]['premium'] = premium
        f.seek(0)
        json.dump(data, f, indent=4)
    return False


# noinspection PyUnusedLocal
class Resume(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    async def on_timeout(self):
        self.clear_items()

    @discord.ui.button(label="Resume", style=discord.ButtonStyle.blurple)
    async def _resume(self, button: discord.ui.Button, interaction: Interaction):
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
    async def _yes(self, button: discord.ui.Button, interaction: Interaction):
        self.value = True
        self.stop()

    @discord.ui.button(label="No", style=discord.ButtonStyle.green)
    async def _no(self, button: discord.ui.Button, interaction: Interaction):
        await interaction.response.send_message(f"Okay, we won't do that then!", ephemeral=True)
        self.value = False
        self.stop()

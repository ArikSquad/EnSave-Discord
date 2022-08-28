# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# Terrible code, so I won't be documenting this. I will probably fix this code to use a data file later
# -----------------------------------------------------------

import json

from utils import db


def get_owner() -> list:
    with open('data/config.json', 'r') as f:
        config = json.load(f)
    owners = []
    for owner in config['owner']:
        owners.append(int(owner))
    return owners


# These will be removed later, after week of warnings.
def get_prefix(ctx, message):
    return db.get_guild_prefix(message.guild.id)


def get_prefix_id(guild_id):
    prefix = db.get_guild_prefix(guild_id)
    return prefix


def set_prefix(guild_id, prefix) -> None:
    db.set_guild_prefix(guild_id, prefix)


def get_id():
    with open('data/config.json', 'r') as f:
        config = json.load(f)
    return config['bot_id']


def set_premium(user_id, premium: bool = True) -> None:
    value = 1 if premium else 0
    db.set_user_premium(user_id, value)

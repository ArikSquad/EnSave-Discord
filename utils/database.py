# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

import datetime
import json


def get_time():
    return datetime.datetime.utcnow()


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

    if str(user_id) in data:
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

# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2021-2023 MikArt
# Released under the Apache License 2.0
#
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


def set_premium(user_id, premium: bool = True) -> None:
    db.set_user_premium(user_id, 1 if premium else 0)

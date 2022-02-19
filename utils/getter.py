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


def get_time():
    return datetime.datetime.utcnow()


def get_guild_ids():
    return [770634445370687519]


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


def premium_embed_interaction(interaction, title: str):
    return nextcord.Embed(title=title,
                          description="You need to be a premium user to use this command.",
                          color=interaction.user.color,
                          timestamp=get_time())


def premium_ad_embed(ctx, title: str):
    return nextcord.Embed(title=title,
                          description=f"If you want more command's get bot premium!.",
                          color=ctx.author.color,
                          timestamp=get_time())


def premium_ad_embed_interaction(interaction, title: str):
    return nextcord.Embed(title=title,
                          description=f"If you want more command's get bot premium!.",
                          color=interaction.user.color,
                          timestamp=get_time())


def get_language(language: str):
    if language.lower == "finnish":
        return "fi_FI"
    elif language.lower == "german":
        return "de_DE"
    elif language.lower == "spanish":
        return "es_ES"
    elif language.lower == "italian":
        return "it_IT"
    elif language.lower == "japanese":
        return "ja_JP"
    elif language.lower == "korean":
        return "ko_KR"
    elif language.lower == "russian":
        return "ru_RU"
    elif language.lower == "chinese":
        return "zh_CN"
    elif language.lower == "polish":
        return "pl_PL"
    elif language.lower == "portuguese":
        return "pt_PT"
    elif language.lower == "dutch":
        return "nl_NL"
    return language

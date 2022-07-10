from sqlite3 import connect

from apscheduler.triggers.cron import CronTrigger

DB_PATH = "data/db/database.db"

cxn = connect(DB_PATH, check_same_thread=False)
cur = cxn.cursor()


def commit():
    cxn.commit()


def autosave(sched):
    sched.add_job(commit, CronTrigger(second=0))


def close():
    cxn.close()


def field(command, *values) -> str:
    cur.execute(command, tuple(values))

    if (fetch := cur.fetchone()) is not None:
        return fetch[0]


def record(command, *values) -> int:
    cur.execute(command, tuple(values))

    return cur.fetchone()


def records(command, *values) -> list:
    cur.execute(command, tuple(values))

    return cur.fetchall()


def column(command, *values) -> list:
    cur.execute(command, tuple(values))

    return [item[0] for item in cur.fetchall()]


def execute(command, *values):
    cur.execute(command, tuple(values))


def multiexec(command, valueset):
    cur.executemany(command, valueset)


def scriptexec(path):
    with open(path, "r", encoding="utf-8") as script:
        cur.executescript(script.read())


def get_user_premium(user_id: int) -> bool:
    return True if int(field("SELECT premium FROM user WHERE userID = ?", user_id)) == 1 else False


def set_user_premium(user_id: int, premium: int) -> None:
    execute("UPDATE user SET premium = ? WHERE userID = ?", premium, user_id)


def get_guild_spy(guild_id: int) -> bool:
    return True if int(field("SELECT spy FROM guild WHERE guildID = ?", guild_id)) == 1 else False


def set_guild_spy(guild_id: int, spy: int) -> None:
    execute("UPDATE guild SET spy = ? WHERE guildID = ?", spy, guild_id)


def get_guild_spy_channel(guild_id: int) -> int:
    return field("SELECT channel FROM guild WHERE guildID = ?", guild_id)


def set_guild_spy_channel(guild_id: int, channel: int) -> None:
    execute("UPDATE guild SET channel = ? WHERE guildID = ?", channel, guild_id)


def get_guild_prefix(guild_id: int) -> str:
    return str(field("SELECT prefix FROM guild WHERE guildID = ?", guild_id))


def set_guild_prefix(guild_id: int, prefix: str) -> None:
    execute("UPDATE guild SET prefix = ? WHERE guildID = ?", prefix, guild_id)


def remove_guild(guild_id: int) -> None:
    execute("DELETE FROM guild WHERE guildID = ?", guild_id)


def get_codes() -> list:
    return records("SELECT secret FROM code")


def add_code(code: str) -> None:
    execute("INSERT OR IGNORE INTO code (secret) VALUES (?)", code)


def remove_code(code: str) -> None:
    execute("DELETE FROM code WHERE secret = ?", code)


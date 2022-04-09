# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

import git
from discord.ext import commands

from utils import database


async def pull(bot):
    repo = git.Repo(".git")
    repo.remotes.origin.pull()
    print("[Git] Pulled from remote.")
    await bot.close()


class Git(commands.Cog, description="Github"):
    EMOJI = "🎈"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pull", hidden=True)
    async def pull(self, ctx):
        if ctx.author.id in database.get_owners_id():
            await pull(self.bot)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == 962313825464504360:
            if message.author.id == 962313982746714142:
                emoji = self.bot.get_emoji(854963304227930123)
                await message.add_reaction(emoji)
                await pull(self.bot)


async def setup(bot):
    await bot.add_cog(Git(bot))

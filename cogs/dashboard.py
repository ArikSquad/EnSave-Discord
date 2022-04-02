# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

from discord.ext import commands, ipc

from utils import database
from utils.website import dashboard


class Dashboard(commands.Cog, description="Customizing dashboard."):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(dashboard.app.run_task(port=1331))

    @ipc.server.route()
    async def get_guild_count(self, data):
        return len(self.bot.guilds)

    @ipc.server.route()
    async def get_guilds(self, data):
        final = []
        for guild in self.bot.guilds:
            final.append(guild.id)
        return final

    @ipc.server.route()
    async def get_guild(self, data):
        guild = self.bot.get_guild(data.guild_id)
        if guild is None:
            return None

        guild_data = {
            "name": guild.name,
            "id": guild.id,
            "prefix": database.get_prefix_by_id(guild.id),
        }

        return guild_data


async def setup(bot):
    await bot.add_cog(Dashboard(bot))

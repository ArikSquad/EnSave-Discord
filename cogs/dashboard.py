# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import discord
from discord.ext import commands, ipc

from utils import database
from utils.website import dashboard


class Dashboard(commands.Cog, description="Custom dashboard"):
    EMOJI = "📊"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(dashboard.app.run_task(host="0.0.0.0", port=1201))

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
            "member_count": len(guild.members),
            "description": guild.description,
            "icon": guild.icon.url,
        }

        return guild_data

    @ipc.server.route()
    async def get_user_name(self, data):
        user = self.bot.get_user(data)
        if user is None:
            return None
        return user.name

    @commands.command(name="dashboard", aliases=["dash"], description="Open the dashboard")
    async def dashboard_command(self, ctx):
        embed = discord.Embed(
            title="Dashboard",
            description="[Click here to open the dashboard](https://ensave.mikart.eu/)",
            color=0x00ff00,
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Dashboard(bot))

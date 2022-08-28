# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import discord
from discord import app_commands
from discord.ext import commands, ipc

from utils import db


class Dashboard(commands.Cog, description="Custom dashboard"):
    def __init__(self, bot):
        self.bot = bot

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
            "prefix": db.get_guild_prefix(guild.id),
            "member_count": len(guild.members)
        }

        return guild_data

    @ipc.server.route()
    async def get_member(self, data):
        user = self.bot.get_user(data.member_id)

        if user is None:
            return None

        member_data = {
            "name": user.name,
            "id": user.id,
            "discriminator": user.discriminator,
            "avatar": user.avatar.url,
            "bot": user.bot,
        }

        return member_data

    # Command to open the dashboard
    @app_commands.command(name="dashboard", description="Open the dashboard")
    async def dashboard_command(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Dashboard",
            description="[Click here to open the dashboard](https://ensave.mikart.eu/)",
            color=discord.Color.from_rgb(48, 50, 54),
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Dashboard(bot))

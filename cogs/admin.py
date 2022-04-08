# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import json

import discord
import psutil as psutil
from discord.ext import commands

from utils import database


class Admin(commands.Cog, description="Gather information"):
    COG_EMOJI = "📜"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", aliases=["information", "about"], help="Gather information about the bot.",
                      hidden=True)
    async def info(self, ctx, user: discord.User = None):
        if user is None and ctx.author.id in database.get_owners_id():
            embed = discord.Embed(title="Information", color=ctx.author.color)
            embed.add_field(name="Authors", value=str(database.get_owners_discord())[1:-1], inline=False)
            embed.add_field(name="Author IDs", value=str(database.get_owners_id())[1:-1], inline=False)
            embed.add_field(name="Library", value="discord")
            embed.add_field(name="Version", value=discord.__version__)
            embed.add_field(name="Guilds", value=len(self.bot.guilds))
            embed.add_field(name="Users", value=len(self.bot.users))
            embed.add_field(name="Latency", value=f"{self.bot.latency * 1000:.2f}ms")
            embed.add_field(name="Memory", value=str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB",
                            inline=False)
            embed.add_field(name="OS Last Boot", value=f"{psutil.boot_time()}")
            embed.add_field(name="CPU Percentage", value=f"{psutil.cpu_percent()}%")
            return await ctx.send(embed=embed)
        elif user is not None and ctx.author.id in database.get_owners_id():
            with open("db/users.json", "r") as f:
                data = json.load(f)
                exp = data[str(ctx.author.id)]['experience']
                level = data[str(ctx.author.id)]['level']
            embed = discord.Embed(title="Information", color=user.color)
            embed.set_thumbnail(url=user.avatar.url)
            embed.add_field(name="Username", value=user.name)
            embed.add_field(name="Discriminator", value=user.discriminator, inline=False)
            embed.add_field(name="ID", value=user.id, inline=False)
            embed.add_field(name="Created at", value=user.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
            embed.add_field(name="Experience", value=exp if exp is not None else "None")
            embed.add_field(name="Level", value=level if level is not None else "None")
            embed.add_field(name="Premium", value="Yes" if database.get_premium(user.id) is True else "No",
                            inline=False)
            embed.add_field(name="Bot Status", value="Yes" if user.bot is True else "No", inline=False)
            embed.add_field(name="Bot Owner", value="Yes" if user.id in database.get_owners_id() else "No",
                            inline=False)
            await ctx.send(embed=embed)

    @commands.command(name='set-premium', help='Set premium state of a user.', hidden=True)
    async def set_premium(self, ctx, user: discord.Member, state: bool = None):
        if ctx.author.id in database.get_owners_id():
            if user.id in database.get_owners_id():
                await ctx.send("You can't set the premium state of an owner.")
            else:
                if state:
                    database.set_premium(user.id, state)
                else:
                    database.set_premium(user.id)
                await ctx.send(f"{user.mention}'s new state of premium: {state}")


async def setup(bot):
    await bot.add_cog(Admin(bot))

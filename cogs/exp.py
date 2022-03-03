# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import json

import nextcord
from nextcord.ext import commands

from utils import database


async def add_exp_on_message(message):
    with open('db/users.json', 'r') as f:
        data = json.load(f)
        if str(message.author.id) in data:
            old_exp = data[str(message.author.id)]['experience']

    amount = 3.5 * len(message.clean_content)
    if len(message.clean_content) > 42:
        amount = 142
    with open('db/users.json', 'r+') as f:
        data = json.load(f)
        if str(message.author.id) not in data:
            data[str(message.author.id)]['experience'] = 0
            data[str(message.author.id)]['level'] = 0
        else:
            if data[str(message.author.id)]['experience'] >= 1000:
                data[str(message.author.id)]['experience'] = 0
                data[str(message.author.id)]['level'] += 1
            else:
                data[str(message.author.id)]['experience'] += amount
        f.seek(0)
        json.dump(data, f, indent=4)

    if data[str(message.author.id)]['experience'] > 50000 and not database.get_premium(message.author.id):
        database.set_premium(message.author.id, True)
        user_level = nextcord.Embed(
            title=f"EnSave Leveling",
            description='Congratulations, you have earned EnSave Premium!',
            color=message.author.color
        )
        await message.channel.send(embed=user_level)
    elif data[str(message.author.id)]['level'] > old_exp:
        user_level = nextcord.Embed(
            title=f"EnSave Leveling",
            description=f"Congratulations, you have leveled "
                        f"up to level {data[str(message.author.id)]['level']}!",
            color=message.author.color
        )
        await message.channel.send(embed=user_level)


class Experience(commands.Cog, description="Gain levels to get more commands!"):
    COG_EMOJI = "📈"

    def __init__(self, bot):
        self.bot = bot

    # When a message is sent in a guild, add some xp to the user.
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author is not self.bot.user:
            await add_exp_on_message(message)

    @commands.command(name='level', help="Check your level.")
    async def level(self, ctx):
        with open("db/users.json", "r") as f:
            data = json.load(f)
            exp = data[str(ctx.author.id)]['experience']
            level = data[str(ctx.author.id)]['level']

            user_level = nextcord.Embed(
                title=f"{ctx.author.name}'s level",
                description="This user has premium." if database.get_premium(ctx.author.id)
                else "This person is still reaching premium.",
                color=ctx.author.color
            )
            user_level.add_field(name='Level', value=level, inline=False)
            user_level.add_field(name='Experience', value=exp, inline=False)

            await ctx.send(embed=user_level)

    @commands.command(name='leaderboard', help="Check the leaderboard.")
    async def leaderboard(self, ctx):
        with open("db/users.json", "r") as f:
            data = json.load(f)
            users = sorted(data.items(), key=lambda x: x[1]['experience'], reverse=True)
            leaderboard = nextcord.Embed(
                title=f"{ctx.author.name}'s level",
                description="This user has premium." if database.get_premium(ctx.author.id)
                else "This person is still reaching premium.",
                color=ctx.author.color
            )
            for i, user in enumerate(users):
                leaderboard.add_field(name=f"{i + 1}. {user[0]}", value=user[1]['experience'], inline=False)
            await ctx.send(embed=leaderboard)

    @commands.command(name='addexp', help="Add experience to somebody.", hidden=True)
    async def add_exp(self, ctx, user: nextcord.Member, amount: int):
        if ctx.author.id in database.get_owner_ids():
            with open("db/users.json", "r+") as f:
                data = json.load(f)
                data[str(user.id)]['experience'] += amount
                f.seek(0)
                json.dump(data, f, indent=4)
            new_exp_embed = nextcord.Embed(
                title=f"Admin",
                description=f"{ctx.author.name} has added {amount} experience to {user.name}.",
                color=ctx.author.color
            )
            await ctx.send(embed=new_exp_embed)

    @commands.command(name='setexp', help="Set experience to somebody.", hidden=True)
    async def set_exp(self, ctx, user: nextcord.Member, amount: int):
        if ctx.author.id in database.get_owner_ids():
            with open("db/users.json", "r+") as f:
                data = json.load(f)
                data[str(user.id)]['experience'] = amount
                f.seek(0)
                json.dump(data, f, indent=4)
            new_exp_embed = nextcord.Embed(
                title=f"Admin",
                description=f"{ctx.author.name} has set {user.name}'s experience to {amount}.",
                color=ctx.author.color
            )
            await ctx.send(embed=new_exp_embed)

    @commands.command(name='setlevel', help="Set level to somebody.", hidden=True)
    async def set_level(self, ctx, user: nextcord.Member, amount: int):
        if ctx.author.id in database.get_owner_ids():
            with open("db/users.json", "r+") as f:
                data = json.load(f)
                data[str(user.id)]['level'] = amount
                f.seek(0)
                json.dump(data, f, indent=4)
            new_level_embed = nextcord.Embed(
                title=f"Admin",
                description=f"{ctx.author.name} has set {user.name}'s level to {amount}.",
                color=ctx.author.color
            )
            await ctx.send(embed=new_level_embed)

    @commands.command(name='addlevel', help="Add levels to somebody.", hidden=True)
    async def add_level(self, ctx, user: nextcord.Member, amount: int):
        if ctx.author.id in database.get_owner_ids():
            with open("db/users.json", "r+") as f:
                data = json.load(f)
                data[str(user.id)]['level'] += amount
                f.seek(0)
                json.dump(data, f, indent=4)
            new_level_embed = nextcord.Embed(
                title=f"Admin",
                description=f"{ctx.author.name} has added {amount} levels to {user.name}.",
                color=ctx.author.color
            )
            await ctx.send(embed=new_level_embed)

    @commands.command(name='getlevel', help="Get a users level.", hidden=True)
    async def get_level(self, ctx, user: nextcord.Member):
        if ctx.author.id in database.get_owner_ids():
            with open("db/users.json", "r") as f:
                data = json.load(f)
                level = data[str(user.id)]['level']
            level_embed = nextcord.Embed(
                title=f"Admin",
                description=f"{user.name}'s level is {level}.",
                color=ctx.author.color
            )
            await ctx.send(embed=level_embed)

    @commands.command(name='getexp', help="Get a users experience.", hidden=True)
    async def get_exp(self, ctx, user: nextcord.Member):
        if ctx.author.id in database.get_owner_ids():
            with open("db/users.json", "r") as f:
                data = json.load(f)
                exp = data[str(user.id)]['experience']
            exp_embed = nextcord.Embed(
                title=f"Admin",
                description=f"{user.name}'s experience is {exp}.",
                color=ctx.author.color
            )
            await ctx.send(embed=exp_embed)


def setup(bot):
    bot.add_cog(Experience(bot))

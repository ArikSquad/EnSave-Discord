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
    amount = 3.5 * len(message.clean_content)
    if amount > 75:
        amount = 75
    with open('db/users.json', 'r+') as f:
        data = json.load(f)
        if str(message.author.id) not in data:
            data[str(message.author.id)] = {}
            data[str(message.author.id)]['experience'] = 1
            data[str(message.author.id)]['level'] = 0
            data[str(message.author.id)]['sent'] = 1
        else:
            if data[str(message.author.id)]['experience'] > 1000:
                data[str(message.author.id)]['experience'] = 0
                data[str(message.author.id)]['level'] = data[str(message.author.id)]['level'] + 1
                data[str(message.author.id)]['sent'] = 0
            else:
                data[str(message.author.id)]['experience'] = data[str(message.author.id)]['experience'] + amount
            f.seek(0)
        json.dump(data, f, indent=4, sort_keys=True)

    if data[str(message.author.id)]['level'] > 50 and not database.get_premium(message.author.id):
        database.set_premium(message.author.id, True)
        user_level = nextcord.Embed(
            title=f"EnSave Leveling",
            description='Congratulations, you have earned EnSave Premium!',
            color=message.author.color
        )
        await message.channel.send(embed=user_level)
    elif data[str(message.author.id)]['sent'] == 0:
        user_level = nextcord.Embed(
            title=f"EnSave Leveling",
            description=f"Congratulations, you have leveled "
                        f"up to level {data[str(message.author.id)]['level']}!",
            color=message.author.color
        )
        await message.channel.send(embed=user_level)
        data[str(message.author.id)]['sent'] = 1
        f.seek(0)
        json.dump(data, f, indent=4, sort_keys=True)
        f.truncate()


def get_level(ctx):
    with open('db/users.json', 'r') as f:
        data = json.load(f)
        return data[str(ctx.author.id)]['level']


def get_xp(ctx):
    with open('db/users.json', 'r') as f:
        data = json.load(f)
        return data[str(ctx.author.id)]['experience']


class Experience(commands.Cog, description="Gain levels to get more commands!"):
    COG_EMOJI = "📈"

    def __init__(self, bot):
        self.bot = bot

    # When a message is sent in a guild, add some xp to the user.
    @commands.Cog.listener()
    async def on_message(self, message):
        time = 1
        with open('db/prefixes.json', 'r') as f:
            prefixes = json.load(f)
            prefix = prefixes[str(message.guild.id)]
        if not message.content.startswith(prefix) and message.author.id != 812808865728954399:
            await add_exp_on_message(message)

    @commands.command(name='level', help="Check your level.")
    async def level(self, ctx):
        user_level = nextcord.Embed(
            title=f"{ctx.author.name}'s level",
            description="This user has gotten premium." if database.get_premium(ctx.author.id)
            else "This person is still reaching premium.",
            color=ctx.author.color
        )
        user_level.add_field(name='Level', value=get_level(ctx), inline=False)
        user_level.add_field(name='Experience', value=get_level(ctx), inline=False)

        await ctx.send(embed=user_level)

    @commands.command(name='addexp', help="Add experience to somebody.", hidden=True)
    async def add_exp(self, ctx, user: nextcord.Member, amount: int):
        if ctx.author.id in database.get_owners_id():
            with open("db/users.json", "r+") as f:
                data = json.load(f)
                data[str(user.id)]['experience'] = data[str(user.id)]['experience'] + amount
                f.seek(0)
                json.dump(data, f, indent=4, sort_keys=True)
                f.truncate()
            new_exp_embed = nextcord.Embed(
                title=f"Admin",
                description=f"{ctx.author.name} has added {amount} experience to {user.name}.",
                color=ctx.author.color
            )
            await ctx.send(embed=new_exp_embed)

    @commands.command(name='setexp', help="Set experience to somebody.", hidden=True)
    async def set_exp(self, ctx, user: nextcord.Member, amount: int):
        if ctx.author.id in database.get_owners_id():
            with open("db/users.json", "r+") as f:
                data = json.load(f)
                data[str(user.id)]['experience'] = amount
                f.seek(0)
                json.dump(data, f, indent=4, sort_keys=True)
                f.truncate()
            new_exp_embed = nextcord.Embed(
                title=f"Admin",
                description=f"{ctx.author.name} has set {user.name}'s experience to {amount}.",
                color=ctx.author.color
            )
            await ctx.send(embed=new_exp_embed)

    @commands.command(name='setlevel', help="Set level to somebody.", hidden=True)
    async def set_level(self, ctx, user: nextcord.Member, amount: int):
        if ctx.author.id in database.get_owners_id():
            with open("db/users.json", "r+") as f:
                data = json.load(f)
                data[str(user.id)]['level'] = amount
                f.seek(0)
                json.dump(data, f, indent=4, sort_keys=True)
                f.truncate()
            new_level_embed = nextcord.Embed(
                title=f"Admin",
                description=f"{ctx.author.name} has set {user.name}'s level to {amount}.",
                color=ctx.author.color
            )
            await ctx.send(embed=new_level_embed)

    @commands.command(name='addlevel', help="Add levels to somebody.", hidden=True)
    async def add_level(self, ctx, user: nextcord.Member, amount: int):
        if ctx.author.id in database.get_owners_id():
            with open("db/users.json", "r+") as f:
                data = json.load(f)
                data[str(user.id)]['level'] = data[str(user.id)]['level'] + amount
                f.seek(0)
                json.dump(data, f, indent=4, sort_keys=True)
                f.truncate()
            new_level_embed = nextcord.Embed(
                title=f"Admin",
                description=f"{ctx.author.name} has added {amount} levels to {user.name}.",
                color=ctx.author.color
            )
            await ctx.send(embed=new_level_embed)

    @commands.command(name='getlevel', help="Get a users level.", hidden=True)
    async def get_level(self, ctx, user: nextcord.Member):
        if ctx.author.id in database.get_owners_id():
            with open("db/users.json", "r") as f:
                data = json.load(f)
                level = data[str(user.id)]['level']
            level_embed = nextcord.Embed(
                title=f"Admin",
                description=f"{user.name}'s level is {level}.",
                color=ctx.author.color
            )
            await ctx.send(embed=level_embed)
            f.truncate()

    @commands.command(name='getexp', help="Get a users experience.", hidden=True)
    async def get_exp(self, ctx, user: nextcord.Member):
        if ctx.author.id in database.get_owners_id():
            with open("db/users.json", "r") as f:
                data = json.load(f)
                exp = data[str(user.id)]['experience']
            exp_embed = nextcord.Embed(
                title=f"Admin",
                description=f"{user.name}'s experience is {exp}.",
                color=ctx.author.color
            )
            await ctx.send(embed=exp_embed)
            f.truncate()


def setup(bot):
    bot.add_cog(Experience(bot))

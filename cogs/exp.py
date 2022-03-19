# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import json

import discord
from PIL import Image, ImageDraw, ImageFont
from discord.ext import commands
from tabulate import tabulate

from utils import database


async def add_exp_on_message(message):
    amount = 3.5 * len(message.clean_content)
    if amount > 75:
        amount = 75
    with open('db/users.json', 'r+') as f:
        data = json.load(f)
        if data[str(message.author.id)]['experience'] > 1000:
            data[str(message.author.id)]['experience'] = 0
            data[str(message.author.id)]['level'] = data[str(message.author.id)]['level'] + 1
            data[str(message.author.id)]['sent'] = 0
        else:
            data[str(message.author.id)]['experience'] = data[str(message.author.id)]['experience'] + amount
        f.seek(0)
        json.dump(data, f, indent=4)

        if data[str(message.author.id)]['level'] > 50 and not database.get_premium(message.author.id):
            database.set_premium(message.author.id, True)
            user_level = discord.Embed(
                title=f"EnSave Leveling",
                description='Congratulations, you have earned EnSave Premium!',
                color=message.author.color
            )
            await message.channel.send(embed=user_level)
        elif data[str(message.author.id)]['sent'] == 0:
            user_level = discord.Embed(
                title=f"EnSave Leveling",
                description=f"Congratulations, you have leveled "
                            f"up to level {data[str(message.author.id)]['level']}!",
                color=message.author.color
            )
            await message.channel.send(embed=user_level)
            data[str(message.author.id)]['sent'] = 1
            f.seek(0)
            json.dump(data, f, indent=4)


def get_level(author_id):
    with open('db/users.json', 'r') as f:
        data = json.load(f)
        return data[str(author_id)]['level']


def get_xp(author_id):
    with open('db/users.json', 'r') as f:
        data = json.load(f)
        return data[str(author_id)]['experience']


class Experience(commands.Cog, description="Gain levels to get more commands!"):
    COG_EMOJI = "📈"

    def __init__(self, bot):
        self.bot = bot

    # When a message is sent in a guild, add some xp to the user.
    @commands.Cog.listener()
    async def on_message(self, message):
        with open('db/prefixes.json', 'r') as f:
            prefixes = json.load(f)
            prefix = prefixes[str(message.guild.id)]
        if not message.content.startswith(prefix) and message.author.id != 812808865728954399 \
                and not message.author.bot and message.guild.id == 770634445370687519:
            await add_exp_on_message(message)

    @commands.command(name='level', help="Check your level.")
    async def level(self, ctx):
        if ctx.guild.id == 770634445370687519:
            user_level = discord.Embed(
                title=f"{ctx.author.name}'s level",
                description="This user has gotten premium." if database.get_premium(ctx.author.id)
                else "This person is still reaching premium.",
                color=ctx.author.color
            )
            user_level.add_field(name='Level', value=get_level(ctx.author.id), inline=False)
            user_level.add_field(name='Experience', value=get_level(ctx.author.id), inline=False)

            await ctx.send(embed=user_level)

    @commands.command(name='addexp', help="Add experience to somebody.", hidden=True, guild_ids=[770634445370687519])
    async def add_exp(self, ctx, user: discord.Member, amount: int):
        if ctx.author.id in database.get_owners_id():
            with open("db/users.json", "r+") as f:
                data = json.load(f)
                data[str(user.id)]['experience'] = data[str(user.id)]['experience'] + amount
                f.seek(0)
                json.dump(data, f, indent=4)
            new_exp_embed = discord.Embed(
                title=f"Admin",
                description=f"{ctx.author.name} has added {amount} experience to {user.name}.",
                color=ctx.author.color
            )
            await ctx.send(embed=new_exp_embed)

    @commands.command(name='setexp', help="Set experience to somebody.", hidden=True)
    async def set_exp(self, ctx, user: discord.Member, amount: int):
        if ctx.author.id in database.get_owners_id():
            with open("db/users.json", "r+") as f:
                data = json.load(f)
                data[str(user.id)]['experience'] = amount
                f.seek(0)
                json.dump(data, f, indent=4)
            new_exp_embed = discord.Embed(
                title=f"Admin",
                description=f"{ctx.author.name} has set {user.name}'s experience to {amount}.",
                color=ctx.author.color
            )
            await ctx.send(embed=new_exp_embed)

    @commands.command(name='setlevel', help="Set level to somebody.", hidden=True)
    async def set_level(self, ctx, user: discord.Member, amount: int):
        if ctx.author.id in database.get_owners_id():
            with open("db/users.json", "r+") as f:
                data = json.load(f)
                data[str(user.id)]['level'] = amount
                f.seek(0)
                json.dump(data, f, indent=4)
            new_level_embed = discord.Embed(
                title=f"Admin",
                description=f"{ctx.author.name} has set {user.name}'s level to {amount}.",
                color=ctx.author.color
            )
            await ctx.send(embed=new_level_embed)

    @commands.command(name='addlevel', help="Add levels to somebody.", hidden=True)
    async def add_level(self, ctx, user: discord.Member, amount: int):
        if ctx.author.id in database.get_owners_id():
            with open("db/users.json", "r+") as f:
                data = json.load(f)
                data[str(user.id)]['level'] = data[str(user.id)]['level'] + amount
                f.seek(0)
                json.dump(data, f, indent=4)
            new_level_embed = discord.Embed(
                title=f"Admin",
                description=f"{ctx.author.name} has added {amount} levels to {user.name}.",
                color=ctx.author.color
            )
            await ctx.send(embed=new_level_embed)

    @commands.command(name='getlevel', help="Get a users level.", hidden=True)
    async def get_level(self, ctx, user: discord.Member):
        if ctx.author.id in database.get_owners_id():
            with open("db/users.json", "r") as f:
                data = json.load(f)
                level = data[str(user.id)]['level']
            level_embed = discord.Embed(
                title=f"Admin",
                description=f"{user.name}'s level is {level}.",
                color=ctx.author.color
            )
            await ctx.send(embed=level_embed)

    @commands.command(name='getexp', help="Get a users experience.", hidden=True)
    async def get_exp(self, ctx, user: discord.Member):
        if ctx.author.id in database.get_owners_id():
            with open("db/users.json", "r") as f:
                data = json.load(f)
                exp = data[str(user.id)]['experience']
            exp_embed = discord.Embed(
                title=f"Admin",
                description=f"{user.name}'s experience is {exp}.",
                color=ctx.author.color
            )
            await ctx.send(embed=exp_embed)

    @commands.command(name='leaderboard', help="Get the leaderboard.", hidden=True)
    async def leaderboard(self, ctx):
        with open("db/users.json", "r") as f:
            data = json.load(f)

        user_ids = list(data.keys())
        user_exp = [data[user_id]['experience'] for user_id in user_ids]
        user_level = [data[user_id]['level'] for user_id in user_ids]

        new_leaderboard = []

        for index, user_id in enumerate(user_ids, 1):
            new_leaderboard.append([user_id, user_level[index - 1], user_exp[index - 1]])

        new_leaderboard.sort(key=lambda x: (x[1], x[2]), reverse=True)

        user_rank_column = []
        user_name_column = []
        user_level_column = []
        user_exp_column = []

        for index, rank_value in enumerate(new_leaderboard[:10]):
            user_rank_column.append([index + 1])

        for index, name_value in enumerate(new_leaderboard[:10]):
            user_name_column.append([await self.bot.fetch_user(name_value[0])])

        for level_index, level_value in enumerate(new_leaderboard[:10]):
            user_level_column.append([level_value[1]])

        for exp_index, exp_value in enumerate(new_leaderboard[:10]):
            user_exp_column.append([exp_value[2]])

        user_rank_table = tabulate(user_rank_column, tablefmt='plain', headers=['#\n'], numalign="left")
        user_name_table = tabulate(user_name_column, tablefmt='plain', headers=['Name\n'], numalign="left")
        user_level_table = tabulate(user_level_column, tablefmt='plain', headers=['Levels\n'], numalign="left")
        user_exp_table = tabulate(user_exp_column, tablefmt='plain', headers=['Experience\n'], numalign="left")

        image_template = Image.open("assets/leaderboard_temp.png")
        font = ImageFont.truetype("assets/leaderboard_temp.ttf", 160)

        rank_text_position = 90, 50
        name_text_position = 400, 50
        level_text_position = 1990, 50
        exp_text_position = 2750, 50

        draw_on_image = ImageDraw.Draw(image_template)
        draw_on_image.text(rank_text_position, user_rank_table, 'white', font=font)
        draw_on_image.text(name_text_position, user_name_table, 'white', font=font)
        draw_on_image.text(level_text_position, user_level_table, 'white', font=font)
        draw_on_image.text(exp_text_position, user_exp_table, 'white', font=font)

        image_template.convert('RGB').save("assets/current_leaderboard.jpg", 'JPEG')

        embed = discord.Embed(
            title="Leaderboard",
            description=f"Here is the current leaderboard.",
            color=ctx.author.color
        )
        embed.set_image(url="attachment://current_leaderboard.jpg")
        await ctx.send(file=discord.File("assets/current_leaderboard.jpg"), embed=embed)


async def setup(bot):
    await bot.add_cog(Experience(bot))

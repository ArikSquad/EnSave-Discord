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


async def get_leaderboard():
    with open('db/users.json', 'r') as f:
        data = json.load(f)
    users = []
    for user in data:
        users.append([user, data[user]['messages']])
    users.sort(key=lambda x: x[1], reverse=True)
    users_top = users[:10]
    return users_top


async def check_message(message):
    with open('db/users.json', 'r') as f:
        data = json.load(f)
    data[str(message.author.id)]["messages"] = data[str(message.author.id)]["messages"] + 1

    with open('db/users.json', 'w') as f:
        f.seek(0)
        json.dump(data, f, indent=4)


def get_amount(author_id: discord.Member):
    with open('db/users.json', 'r') as f:
        data = json.load(f)
    level = data[str(author_id)]['messages']
    f.close()
    return level


def set_amount(author_id: discord.Member, amount: int):
    with open('db/users.json', 'r') as f:
        data = json.load(f)
    data[str(author_id)]['messages'] = amount
    with open('db/users.json', 'w') as f:
        f.seek(0)
        json.dump(data, f, indent=4)
    f.close()


def add_amount(author_id: discord.Member, amount: int):
    with open('db/users.json', 'r') as f:
        data = json.load(f)
    data[str(author_id)]['messages'] = data[str(author_id)]['messages'] + amount
    with open('db/users.json', 'w') as f:
        f.seek(0)
        json.dump(data, f, indent=4)
    f.close()


class Messages(commands.Cog, description="Send messages and see how many you have sent"):
    EMOJI = "📈"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        with open('db/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefix = prefixes[str(message.guild.id)] if message.guild is not None else "."

        if not message.content.startswith(prefix) and message.author.id != 812808865728954399 \
                and not message.author.bot:
            await check_message(message)

    @commands.command(name='messages', help="Check your message count.")
    async def messages(self, ctx):
        user_level = discord.Embed(
            title=f"{ctx.author.name}'s Message Count",
            description="This user has gotten premium." if database.get_premium(ctx.author.id)
            else "This person is still reaching premium.",
            color=ctx.author.color
        )
        user_level.add_field(name='Messages', value=get_amount(ctx.author.id), inline=False)

        await ctx.send(embed=user_level)

    @commands.command(name='addexp', help="Add the count of messages an user has sent.",
                      hidden=True)
    async def add_exp(self, ctx, user: discord.Member, amount: int):
        if ctx.author.id in database.get_owner_ids():
            add_amount(user.id, amount)
            new_exp_embed = discord.Embed(
                title=f"Admin",
                description=f"{ctx.author.name} has added {amount} experience to {user.name}.",
                color=ctx.author.color
            )
            await ctx.send(embed=new_exp_embed)

    @commands.command(name='setmessages', help="Set the count of messages an user has sent.",
                      hidden=True)
    async def set_exp(self, ctx, user: discord.Member, amount: int):
        if ctx.author.id in database.get_owner_ids():
            set_amount(user.id, amount)
            new_exp_embed = discord.Embed(
                title=f"Admin",
                description=f"{ctx.author.name} has set {user.name}'s experience to {amount}.",
                color=ctx.author.color
            )
            await ctx.send(embed=new_exp_embed)

    @commands.command(name='getmessage', help="Get an user's experience count.", hidden=True)
    async def get_messages(self, ctx, user: discord.Member):
        if ctx.author.id in database.get_owner_ids():
            amount = get_amount(user.id)
            exp_embed = discord.Embed(
                title=f"Admin",
                description=f"{user.name} has sent {amount} messages.",
                color=ctx.author.color
            )
            await ctx.send(embed=exp_embed)

    @commands.command(name='leaderboard',
                      help="Get the top 10 users who have messages the most in the servers that has this bot.",
                      brief="Leaderboard of 10 user's message count.",
                      hidden=True)
    async def leaderboard(self, ctx):
        with open("db/users.json", "r") as f:
            data = json.load(f)

        user_ids = list(data.keys())
        user_messages = [data[user_id]['messages'] for user_id in user_ids]

        new_leaderboard = []

        for index, user_id in enumerate(user_ids, 1):
            new_leaderboard.append([user_id, user_messages[index - 1]])

        new_leaderboard.sort(key=lambda x: x[1], reverse=True)

        user_rank_column = []
        user_name_column = []
        user_msg_column = []

        for index, rank_value in enumerate(new_leaderboard[:10]):
            user_rank_column.append([index + 1])

        for index, name_value in enumerate(new_leaderboard[:10]):
            user_name_column.append([await self.bot.fetch_user(name_value[0])])

        for exp_index, msg_value in enumerate(new_leaderboard[:10]):
            user_msg_column.append([msg_value[1]])

        user_rank_table = tabulate(user_rank_column, tablefmt='plain', headers=['#\n'], numalign="left")
        user_name_table = tabulate(user_name_column, tablefmt='plain', headers=['Name\n'], numalign="left")
        user_msg_table = tabulate(user_msg_column, tablefmt='plain', headers=['Messages\n'], numalign="left")

        image_template = Image.open("assets/background.png")
        font = ImageFont.truetype("assets/leaderboard_temp.ttf", 160)

        rank_text_position = 90, 50
        name_text_position = 400, 50
        exp_text_position = 1990, 50  # Old: 2750, 50

        draw_on_image = ImageDraw.Draw(image_template)
        draw_on_image.text(rank_text_position, user_rank_table, 'white', font=font)
        draw_on_image.text(name_text_position, user_name_table, 'white', font=font)
        draw_on_image.text(exp_text_position, user_msg_table, 'white', font=font)

        image_template.convert('RGB').save("assets/current_leaderboard.jpg", 'JPEG')

        embed = discord.Embed(
            title="Leaderboard",
            description=f"Here is the current leaderboard of most messages sent.",
            color=ctx.author.color
        )
        embed.set_image(url="attachment://current_leaderboard.jpg")
        await ctx.send(file=discord.File("assets/current_leaderboard.jpg"), embed=embed)


async def setup(bot):
    await bot.add_cog(Messages(bot))

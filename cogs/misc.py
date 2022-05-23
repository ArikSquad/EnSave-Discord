# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2021-2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import json
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from utils import database

old_commands = [
    'dice', 'slot', 'cookie', 'coinflip', 'dog', 'invite', 'clear', 'lock', 'unlock', 'changeprefix',
    'mcserver'
]


class Misc(commands.Cog, description="Random commands"):
    EMOJI = "🤖"

    def __init__(self, bot) -> None:
        self.bot = bot

    @app_commands.command(name="dog", description="Posts a fun dog picture in the chat!")
    async def dog(self, interaction: discord.Interaction):
        choice = random.randint(1, 2)
        title_text = "Dog"

        if choice == 1:
            title_text = "Aww cute!"
        elif choice == 2:
            title_text = "Get bot premium for more cool commands!"
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://random.dog/woof.json') as r:
                data = await r.json()
                embed = discord.Embed(
                    title=title_text,
                    color=interaction.user.color
                )
                embed.set_image(url=data['url'])
                await interaction.response.send_message(embed=embed)

    @app_commands.command(name="invite-bot", description='Get the invite link of the bot.')
    async def invite_bot(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title='Info',
            description=f'Invite me by clicking '
                        f'[here](https://discord.com/api/oauth2/authorize?client_id='
                        f'812808865728954399&permissions=8&scope=bot%20applications.commands).',
            color=0xD75BF4
        )
        await interaction.response.send_message(embed=embed)

    @commands.command(name='old_dated_command',
                      aliases=old_commands,
                      help='Remove commands that are unsupported from the list. (Slash commands)', hidden=True)
    async def old_dated(self, ctx: commands.Context):
        embed = discord.Embed(title=f"Slash Commands.",
                              description=f'The command you tried to run is no longer '
                                          f'supported without slash command.',
                              color=ctx.author.color)
        await ctx.reply(embed=embed)

    @commands.command(name='redeem', help="Redeem a code for a reward!", hidden=True)
    async def redeem(self, ctx, code):
        if not database.get_premium(ctx.author.id):
            with open('db/codes.json', 'r') as f:
                codes = json.load(f)

            amount = 0
            # check how many codes are in the file
            for _ in codes["codes"]:
                amount = amount + 1

            # there is probably a better way, but I rushed this code
            success = False
            for i in range(amount):
                if codes["codes"][str(i + 1)][0] == str(code):
                    success = True
                    codes["codes"][str(i + 1)][0] = None
                    with open('db/codes.json', 'w') as f:
                        json.dump(codes, f, indent=4)

            if success:
                try:
                    database.set_premium(ctx.author.id, True)
                except KeyError:
                    await ctx.send("Hey, please contact ArikSquad#6222 to get your price, "
                                   "something went wrong when giving automatically.")
                embed = discord.Embed(
                    title="Success!",
                    description=f"You have redeemed {code}.!",
                    color=ctx.author.color
                )
                await ctx.reply(embed=embed)
                self.bot.get_message()
            else:
                embed = discord.Embed(
                    title="Error",
                    description=f"{ctx.author.mention} You have entered an invalid code!",
                    color=ctx.author.color
                )
                await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description=f"{ctx.author.mention} You are already a premium member!",
                color=ctx.author.color
            )
            await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Misc(bot))

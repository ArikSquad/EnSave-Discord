# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2021-2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from utils import utility, db


class Misc(commands.Cog, description="Random commands"):
    EMOJI = "🤖"

    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(name="dog", description="Posts a fun dog picture in the chat!",
                             help="Posts a fun dog picture in the chat!")
    async def dog(self, ctx: commands.Context):
        title_text = "Dog" if random.randint(1, 2) == 1 else "Doggo"

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://random.dog/woof.json') as r:
                data = await r.json()
                embed = discord.Embed(
                    title=title_text,
                    color=discord.Color.from_rgb(48, 50, 54)
                )
                embed.set_image(url=data['url'])
                await ctx.send(embed=embed)

    @app_commands.command(name="invite-bot", description='Get the invite link of the bot.')
    async def invite_bot(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title='Info',
            description=f'Invite me by clicking '
                        f'[here](https://discord.com/api/oauth2/authorize?client_id='
                        f'812808865728954399&permissions=8&scope=bot%20applications.commands).',
            color=discord.Color.from_rgb(48, 50, 54)
        )
        await interaction.response.send_message(embed=embed)

    @commands.command(name='redeem', help="Redeem a code for a reward!", hidden=True)
    async def redeem(self, ctx, code: str):
        if not db.get_user_premium(ctx.author.id):
            keys = db.get_codes()

            success = False
            if (code,) in keys:
                success = True
                db.remove_code(code)

            if success:
                try:
                    utility.set_premium(ctx.author.id, True)
                except KeyError:
                    await ctx.send("Hey, please contact ArikSquad#6222 to get your premium, "
                                   "something went wrong when giving automatically.")
                embed = discord.Embed(
                    title="Success!",
                    description=f"You have redeemed {code}!",
                    color=discord.Color.from_rgb(48, 50, 54)
                )
                await ctx.reply(embed=embed)
            else:
                embed = discord.Embed(
                    title="Error",
                    description=f"{ctx.author.mention} You have entered an invalid code!",
                    color=discord.Color.from_rgb(48, 50, 54)
                )
                await ctx.reply(embed=embed)
        else:
            embed = discord.Embed(
                title="Error",
                description=f"{ctx.author.mention} You are already a premium access!",
                color=discord.Color.from_rgb(48, 50, 54)
            )
            await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(Misc(bot))

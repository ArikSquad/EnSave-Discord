import random

import aiohttp
import discord
from discord.ext import commands


class Fun(commands.Cog, description="Fun commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Dog picture", name="Dog")
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://random.dog/woof.json") as r:
                data = await r.json()
                embed = discord.Embed(
                    title="Doggo",
                    color=ctx.author.color
                )
                embed.set_image(url=data['url'])

                await ctx.send(embed=embed)

    @commands.command(help="Coinflip", name="Coinflip")
    async def coinflip(self, ctx):

        determine_flip = [1, 0]
        if random.choice(determine_flip) == 1:
            embed = discord.Embed(title="Fun",
                                  description=f"{ctx.author.mention} Flipped coin, we got **Heads**!")
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Fun",
                                  description=f"{ctx.author.mention} Flipped coin, we got **Tails**!")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Fun(bot))

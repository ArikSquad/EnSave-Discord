import asyncio
import datetime
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

    @commands.command(aliases=["co"], name="Cookie")
    async def cookie(self, ctx):
        """Who can catch the cookie first?"""

        m = await ctx.send(embed=discord.Embed(title="🍪 Cookie is coming..."))
        await asyncio.sleep(3)
        for i in range(3, 0, -1):
            await m.edit(embed=discord.Embed(title=f"🍪 Cookie is coming in **{i}**"))
            await asyncio.sleep(1)

        start = datetime.datetime.utcnow()
        await m.add_reaction("🍪")
        try:
            # Now we wait for the reaction
            _, user = await self.bot.wait_for(
                "reaction_add",
                check=lambda r, u: str(r.emoji) == "🍪" 
                                and r.message == m
                                and not u.bot,
                timeout=10,
            )
        except asyncio.TimeoutError:
            await ctx.send("No one got the cookie :(")
        else:
            time = round((datetime.datetime.utcnow() - start).total_seconds() - self.bot.latency, 3)
            await m.edit(embed=discord.Embed(title=f"**{user.display_name}** got the cookie in **{time}** seconds"))

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

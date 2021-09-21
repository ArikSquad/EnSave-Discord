import discord
from discord.ext import commands
import random
import asyncio
import json
import datetime


class Fun(commands.Cog, description="Fun commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Advice")
    async def advice(self, ctx):
        """Gives a random advice"""
        async with self.bot.session.get("https://api.adviceslip.com/advice") as r:
            resp = json.loads(await r.text())
            await ctx.send(embed=discord.Embed(title="Advice", description=resp["slip"]["advice"], color=0x2F3136))

    @commands.command(aliases=["co"], name="Cookie")
    async def cookie(self, ctx):
        """Who can catch the cookie first?"""

        # We send cookie is coming and then wait for 3 seconds
        m = await ctx.send(embed=discord.Embed(title="🍪 Cookie is coming..."))
        await asyncio.sleep(3)

        # Now every second we edit the message till the time is 0
        for i in range(3, 0, -1):
            await m.edit(embed=discord.Embed(title=f"🍪 Cookie is coming in **{i}**"))
            await asyncio.sleep(1)

        # If the time is 0 then we start the challenge
        # First we save the start time
        start = datetime.datetime.utcnow()
        await m.add_reaction("🍪")
        try:
            # Now we wait for the reaction
            _, user = await self.bot.wait_for(
                "reaction_add",  # an reaction is being added
                check=lambda r, u: str(r.emoji) == "🍪"  # the emoji is cookie
                                and r.message == m  # the reaction is on the message we want
                                and not u.bot,  # the reaction was not by a bot
                timeout=10,  # we stop after 10 seconds
            )
        except asyncio.TimeoutError:
            await ctx.send("No one got the cookie :(")
        else:
            time = round((datetime.datetime.utcnow() - start).total_seconds() - self.bot.latency, 3)
            await m.edit(embed=discord.Embed(title=f"**{user.display_name}** got the cookie in **{time}** seconds"))

    @commands.command(help="Coinflip", name="Coinflip")
    async def coinflip(self, ctx):
        """
        Flips coin.
        """

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

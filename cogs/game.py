# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

import asyncio
import datetime
import random

import discord
from discord.ext import commands
from discord_slash import cog_ext

from utils import getter

guild_ids = [770634445370687519]


class Game(commands.Cog, description="Game Commands"):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="rps", guild_ids=guild_ids, description="Rock? Paper? Scissors!")
    async def rps(self, ctx):
        def check_win(p, b):
            if p == '🌑':
                return False if b == '📄' else True
            if p == '📄':
                return False if b == '✂' else True
            return False if b == '🪨' else True

        async with ctx.typing():
            reactions = ['🪨', '📄', '✂']
            game_message = await ctx.send("**Rock Paper Scissors**\nChoose your shape:", delete_after=15.0)
            for reaction in reactions:
                await game_message.add_reaction(reaction)
            bot_emoji = random.choice(reactions)

        def check(reaction2s, user):
            return user != self.bot.user and user == ctx.author and (str(reaction2s.emoji) == '🪨' or '📄' or '✂')

        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Time's Up! :stopwatch:")
        else:
            await ctx.send(f"**YOU:\t{reaction.emoji}\nME:\t{bot_emoji}**")
            if str(reaction.emoji) == bot_emoji:
                embed1 = discord.Embed(title=f"Games", description="**It's a Tie :ribbon:**",
                                       color=discord.Color.gold())
                await ctx.send(embed=embed1)
            elif check_win(str(reaction.emoji), bot_emoji):
                embed2 = discord.Embed(title=f"Games", description="**You win :sparkles:**",
                                       color=discord.Color.green())
                await ctx.send(embed=embed2)
            else:
                embed3 = discord.Embed(title=f"Games", description="**I win :robot:**",
                                       color=discord.Color.red())
                await ctx.send(embed=embed3)

    @cog_ext.cog_slash(name="cookie", guild_ids=guild_ids, description="Cookie game!")
    async def cookie(self, ctx):
        """Who can catch the cookie first?"""

        m = await ctx.send(embed=discord.Embed(title="🍪 Cookie is coming..."))
        await asyncio.sleep(3)

        for i in range(3, 0, -1):
            await m.edit(embed=discord.Embed(title=f"🍪 Cookie is coming in **{i}**"))
            await asyncio.sleep(1)

        start = datetime.datetime.now()
        await m.add_reaction("🍪")
        try:
            _, user = await self.bot.wait_for(
                "reaction_add",
                check=lambda r, u: str(r.emoji) == "🍪" and r.message == m and not u.bot,
                timeout=10,
            )
        except asyncio.TimeoutError:
            prank = await ctx.send("No one got the cookie :(")
            await asyncio.sleep(2)
            prank.edit(content="Just kidding, you got the cookie! :)")
        else:
            time_variable = round((getter.get_time() - start).total_seconds() - self.bot.latency, 3)
            await m.edit(embed=discord.Embed(
                title=f"**{user.display_name}** got the cookie in **{time_variable}** seconds")
            )

    @cog_ext.cog_slash(name="8ball", guild_ids=guild_ids)
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def eightball(self, ctx, *, question: commands.clean_content):
        """ Consult 8ball to receive an answer """
        ballresponse = [
            "Yes", "No", "Take a wild guess...", "Very doubtful",
            "Sure", "Without a doubt", "Most likely", "Might be possible",
            "You'll be the judge", "no... (╯°□°）╯︵ ┻━┻", "no... baka",
            "senpai, pls no ;-;", "I have no idea"
        ]
        answer = random.choice(ballresponse)
        embed1 = discord.Embed(title=f"{question}", description=f":8ball: {answer}",
                               color=ctx.author.color)
        await ctx.send(embed=embed1)

    @cog_ext.cog_slash(name="Slot", guild_ids=guild_ids)
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        embed1 = discord.Embed(title=f"Games", description=f"{slotmachine} All matching, you won! 🎉",
                               color=discord.Color.green())
        embed2 = discord.Embed(title=f"Games", description=f"{slotmachine} 2 in a row, you won! 🎉",
                               color=discord.Color.purple())
        embed3 = discord.Embed(title=f"Games", description=f"{slotmachine} No match, you lost 😢",
                               color=discord.Color.red())

        if a == b == c:
            await ctx.send(embed=embed1)
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(embed=embed2)
        else:
            await ctx.send(embed=embed3)

    @cog_ext.cog_slash(name="Dice", guild_ids=guild_ids)
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def _dice(self, ctx):
        """Roll dice!"""
        embed1 = discord.Embed(title=f"Games", description="Rolled a {}!".format(random.randint(1, 6)),
                               color=discord.Color.green())
        await ctx.send(embed=embed1)

    @cog_ext.cog_slash(name="Slap", guild_ids=guild_ids)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def slap(self, ctx, member: discord.User = None):
        """Slaps someone you select"""
        emb = discord.Embed(title="Games",
                            description=f"{ctx.message.author.mention} slaps {member.mention} in the face!",
                            color=0x3498db)

        await ctx.send(embed=emb)

    @cog_ext.cog_slash(name="Coinflip", guild_ids=guild_ids)
    async def coinflip(self, ctx):
        """Flips a coin"""

        determine_flip = [1, 0]
        if random.choice(determine_flip) == 1:
            embed = discord.Embed(title="Fun",
                                  description=f"{ctx.author.mention} Flipped coin, we got **Heads**!",
                                  color=ctx.author.color)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Fun",
                                  description=f"{ctx.author.mention} Flipped coin, we got **Tails**!",
                                  color=ctx.author.color)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Game(bot))

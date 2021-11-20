import asyncio
import datetime
import random
import secrets

import aiohttp
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

from db import config
from game import tictactoe

guild_ids = [770634445370687519]


class Slash(commands.Cog, description="Slash Commands"):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="dog", guild_ids=guild_ids, description="Dog pictures!")
    async def dog(self, ctx: SlashContext):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://random.dog/woof.json") as r:
                data = await r.json()
                embed = discord.Embed(
                    title="Doggo",
                    color=ctx.author.color
                )
                embed.set_image(url=data['url'])
                await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="Password", guild_ids=guild_ids)
    async def password(self, ctx, nbytes: int = 18):
        """ Generates a random password string for you containing nbytes random bytes.
        """

        embed1 = discord.Embed(title=f"Misc", description="I only accept any numbers between 3-1400",
                               color=discord.Color.dark_red())

        embed2 = discord.Embed(title=f"Misc", description=f"Sending you a private message with your "
                                                          f"random generated password **{ctx.author.name}**",
                               color=discord.Color.green())

        embed3 = discord.Embed(title=f"Misc", description=f"🎁 **Here is your "
                                                          f"password:**\n{secrets.token_urlsafe(nbytes)}",
                               color=discord.Color.green())

        if nbytes not in range(3, 1401):
            return await ctx.send(embed=embed1)
        if hasattr(ctx, "guild") and ctx.guild is not None:
            await ctx.send(embed=embed2)
        await ctx.author.send(embed=embed3)

    @cog_ext.cog_slash(name="rps", guild_ids=guild_ids, description="RockPaperScissors!")
    async def rps(self, ctx):
        def check_win(p, b):
            if p == '🌑':
                return False if b == '📄' else True
            if p == '📄':
                return False if b == '✂' else True
            # p=='✂'
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
            # if conds
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

    @cog_ext.cog_slash(name="tictactoe", guild_ids=guild_ids, description="TicTacToe game!")
    async def ttt(self, ctx):
        """Play Tic-Tac-Toe"""
        await tictactoe.play_game(self.bot, ctx, chance_for_error=0.2)

    @cog_ext.cog_slash(name="cookie", guild_ids=guild_ids, description="Cookie game!")
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
                check=lambda r, u: str(r.emoji) == "🍪" and r.message == m and not u.bot,
                timeout=10,
            )
        except asyncio.TimeoutError:
            await ctx.send("No one got the cookie :(")
        else:
            time = round((datetime.datetime.utcnow() - start).total_seconds() - self.bot.latency, 3)
            await m.edit(embed=discord.Embed(title=f"**{user.display_name}** got the cookie in **{time}** seconds"))

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

        embed1 = discord.Embed(title=f"Games", description=f"🎱 **Question:** {question}\n**Answer:** {answer}",
                               color=discord.Color.green())

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

    @cog_ext.cog_slash(name=config.misc['sayCommandName'], guild_ids=guild_ids)
    async def say(self, ctx, *, text):
        f"""{config.misc['sayCommandDescription']}"""
        msg = discord.Embed(title="Misc",
                            description=f'' + ctx.message.author.mention + ': ' + text,
                            color=discord.Color.green())
        async with ctx.typing():
            await asyncio.sleep(2)
        await ctx.send(embed=msg)

    @cog_ext.cog_slash(name="Hello", guild_ids=guild_ids)
    async def hello(self, ctx):
        """Says hello to you!"""
        msg = discord.Embed(title="Misc",
                            description=f"Hello {ctx.author.name}",
                            color=discord.Color.green())
        await ctx.send(embed=msg)


def setup(bot):
    bot.add_cog(Slash(bot))

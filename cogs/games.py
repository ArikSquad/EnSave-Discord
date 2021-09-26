import random

import discord
from discord.ext import commands

from game import hangman


class Games(commands.Cog, description="Game commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='hangman', aliases=['hang'])
    async def hangman(self, ctx):
        """Play Hangman"""
        await hangman.play(self.bot, ctx)

    # NEED TO BE FIXED
    @commands.command(name='rps', aliases=['rockpaperscissors'])
    async def rps(self, ctx):
        ctx.send("This command is disabled.")
        """
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

        def check(reaction, user):
            return user != self.bot.user and user == ctx.author and (str(reaction.emoji) == '🪨' or '📄' or '✂')

        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Time's Up! :stopwatch:")
        else:
            await ctx.send(f"**YOU:\t{reaction.emoji}\nME:\t{bot_emoji}**")
            # if conds
            if str(reaction.emoji) == bot_emoji:
                embed1 = discord.Embed(title=f"Games", description="**It's a Tie :ribbon:**",
                                       color=discord.Color.gold)

                await ctx.send(embed=embed1)

            elif check_win(str(reaction.emoji), bot_emoji):

                embed2 = discord.Embed(title=f"Games", description="**You win :sparkles:**",
                                       color=discord.Color.green())

                await ctx.send(embed=embed2)

            else:

                embed3 = discord.Embed(title=f"Games", description="**I win :robot:**",
                                       color=discord.Color.red())

                await ctx.send(embed=embed3)
        """

    @commands.command(help="Roll dice!", name="Dice", aliases=["rollingdice", "diceroll", "rolldice"])
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def rolldice(self, ctx):
        """Roll dice!"""
        embed1 = discord.Embed(title=f"Games", description="Rolled a {}!".format(random.randint(1, 6)),
                               color=discord.Color.green())
        await ctx.send(embed=embed1)

    @commands.command(aliases=["8ba"], name="8Ball")
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

    @commands.command(aliases=["slots", "bet"], name="Slot")
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


def setup(bot):
    bot.add_cog(Games(bot))

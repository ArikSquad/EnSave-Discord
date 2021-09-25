import random

import discord
from discord.ext import commands


class Games(commands.Cog, description="Game commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Roll dice!", name="Dice", aliases=["rollingdice", "diceroll", "rolldice"])
    async def rolldice(self, ctx):
        """Roll dice!"""
        await ctx.send("Rolled a {}!".format(random.randint(1, 6)))

    @commands.command(aliases=["8ba"], name="8Ball")
    async def eightball(self, ctx, *, question: commands.clean_content):
        """ Consult 8ball to receive an answer """
        ballresponse = [
            "Yes", "No", "Take a wild guess...", "Very doubtful",
            "Sure", "Without a doubt", "Most likely", "Might be possible",
            "You'll be the judge", "no... (╯°□°）╯︵ ┻━┻", "no... baka",
            "senpai, pls no ;-;"
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

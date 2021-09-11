import discord
from discord.ext import commands
import random


class Info(commands.Cog, description="Fun commands"):
    def __init__(self, bot):
        self.bot = bot


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
    bot.add_cog(Info(bot))

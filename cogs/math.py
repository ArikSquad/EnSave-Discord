import discord
from discord.ext import commands


class Math(commands.Cog, description="Math Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Multiply numbers", name="Multiply")
    async def multiply(self, ctx, left: int, right: int):
        as4 = discord.Embed(title="Maths",
                            description=f"Total: {left * right}! {ctx.message.author.mention}",
                            color=discord.Color.dark_red())
        await ctx.send(embed=as4)

    @commands.command(help="Subtract numbers", name="Subtract")
    async def subtract(self, ctx, left: int, right: int):
        remove = discord.Embed(title="Maths",
                               description=f"Total: {left - right}! {ctx.message.author.mention}",
                               color=discord.Color.dark_red())
        await ctx.send(embed=remove)

    @commands.command(help="Divide numbers", name="Divide")
    async def divide(self, ctx, left: int, right: int):
        divide = discord.Embed(title="Maths",
                               description=f"Total: {left / right}! {ctx.message.author.mention}",
                               color=discord.Color.dark_red())
        await ctx.send(embed=divide)

    @commands.command(help="Add a number to a another number", name="Add")
    async def add(self, ctx, left: int, right: int):

        msg = discord.Embed(title="Maths",
                            description=f"Total: {left + right}! {ctx.message.author.mention}",
                            color=discord.Color.green())

        await ctx.send(embed=msg)


def setup(bot):
    bot.add_cog(Math(bot))

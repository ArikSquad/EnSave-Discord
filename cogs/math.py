import discord
from discord.ext import commands


class Math(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Multiply numbers.", brief="Multiply numbers.")
    async def multiply(self, ctx, left: int, right: int):
        as4 = discord.Embed(title="Maths",
                            description=f"The answer is: {left * right}! {ctx.message.author.mention}",
                            color=discord.Color.dark_red())

        await ctx.message.delete()
        await ctx.send(embed=as4)

    @commands.command(help="Multiply numbers.", brief="Multiply numbers.")
    async def remove(self, ctx, left: int, right: int):
        remove = discord.Embed(title="Maths",
                               description=f"The answer is: {left - right}! {ctx.message.author.mention}",
                               color=discord.Color.dark_red())

        await ctx.message.delete()
        await ctx.send(embed=remove)

    @commands.command(help="Divide numbers.", brief="Divide numbers.")
    async def divide(self, ctx, left: int, right: int):
        divide = discord.Embed(title="Maths",
                               description=f"The answer is: {left / right}! {ctx.message.author.mention}",
                               color=discord.Color.dark_red())

        await ctx.message.delete()
        await ctx.send(embed=divide)

    @commands.command(help="Add a number to a another number.", brief="Add a number to a another number.", )
    async def add(self, ctx, left: int, right: int):
        msg1 = discord.Embed(title="Maths",
                             description=f"Thinking...",
                             color=discord.Color.green())
        ss = await ctx.send(embed=msg1)

        msg = discord.Embed(title="Maths",
                            description=f"The answer is {left + right}! Thanks for asking {ctx.message.author.mention}",
                            color=discord.Color.green())

        no = discord.Embed(title="Maths",
                           description=f"You forgot the numbers! {ctx.message.author.mention}",
                           color=discord.Color.green())

        await ctx.message.delete()

        if left & right is not None:
            await ss.edit(embed=msg)
        else:
            ctx.send(embed=no)


def setup(bot):
    bot.add_cog(Math(bot))

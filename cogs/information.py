# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

import nextcord
import nextcord.utils
from nextcord.ext import commands

from utils import getter


class Information(commands.Cog, description="Gather information."):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", aliases=["information", "about"], help="Gather information about the bot.",
                      hidden=True)
    async def info(self, ctx):
        if ctx.author.id == getter.get_owner_id():
            embed = nextcord.Embed(title="Information", color=ctx.author.color)
            embed.add_field(name="Author", value="ArikSquad#6222")
            embed.add_field(name="Library", value="nextcord")
            embed.add_field(name="Version", value=nextcord.__version__)
            embed.add_field(name="Guilds", value=len(self.bot.guilds))
            embed.add_field(name="Users", value=len(self.bot.users))
            embed.add_field(name="Latency", value=f"{self.bot.latency * 1000:.2f}ms")

            await ctx.send(embed=embed)

    @commands.command(name="eval", help="Evaluate code", hidden=True)
    async def eval(self, ctx, *, code):
        if ctx.author.id == getter.get_owner_id():
            try:
                result = eval(code)
                if result is not None:
                    await ctx.send(f"```py\n{result}```")
            except Exception as e:
                await ctx.send(f"```py\n{e}```")

    @commands.command(name="exec", help="Execute code", hidden=True)
    async def exec(self, ctx, *, code):
        if ctx.author.id == getter.get_owner_id():
            try:
                exec(code)
            except Exception as e:
                await ctx.send(f"```py\n{e}```")

    @commands.command(name="shutdown", help="Shutdown the bot.", hidden=True)
    async def shutdown(self, ctx):
        if ctx.author.id == getter.get_owner_id():
            view = getter.Sure()
            sure = nextcord.Embed(title="Are you sure?", description="This will logout "
                                                                     "from discord and exit the python program.",
                                  color=ctx.author.color)
            message = await ctx.send(embed=sure, view=view)
            await view.wait()
            if view.value is None:
                return
            elif view.value:
                shutting = nextcord.Embed(title="Admin", description="Shutting down...", color=ctx.author.color)
                await message.edit(embed=shutting)
                await self.bot.close()


def setup(bot):
    bot.add_cog(Information(bot))

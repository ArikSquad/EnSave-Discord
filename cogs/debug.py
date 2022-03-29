# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

import discord
from better_profanity import profanity
from discord.ext import commands

from utils import database


class Debug(commands.Cog, description="Debug commands."):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="eval", help="Evaluate code", hidden=True)
    async def eval(self, ctx, *, code):
        if ctx.author.id in database.get_owners_id():
            try:
                result = eval(code)
                if result is not None:
                    await ctx.send(f"```py\n{result}```")
            except Exception as e:
                await ctx.send(f"```py\n{e}```")

    @commands.command(name="exec", help="Execute code", hidden=True)
    async def exec(self, ctx, *, code):
        if ctx.author.id in database.get_owners_id():
            try:
                exec(code)
            except Exception as e:
                await ctx.send(f"```py\n{e}```")

    @commands.command(name="shutdown", help="Shutdown the bot.", hidden=True)
    async def shutdown(self, ctx):
        if ctx.author.id in database.get_owners_id():
            view = database.YesNo()
            sure = discord.Embed(title="Are you sure?", description="This will logout "
                                                                    "from discord and exit the python program.",
                                 color=ctx.author.color)
            message = await ctx.send(embed=sure, view=view)
            await view.wait()
            if view.value is None:
                return
            elif view.value:
                await message.delete()
                await self.bot.close()

    @commands.command(name='unload_cog', help='Unload a cog.', hidden=True)
    async def unload_cog(self, ctx, cog):
        if ctx.author.id in database.get_owners_id():
            try:
                await self.bot.unload_extension(f'cogs.{cog}')
                await ctx.send(f"`{cog}` unloaded.")
            except commands.ExtensionNotFound:
                await ctx.send(f'There is no extension called {profanity.censor(cog)}')
            except commands.ExtensionNotLoaded:
                await ctx.send('The extension is already unloaded.')

    @commands.command(name='load_cog', help='Load a cog.', hidden=True)
    async def load_cog(self, ctx, cog):
        if ctx.author.id in database.get_owners_id():
            try:
                await self.bot.load_extension(f'cogs.{cog}')
                await ctx.send(f'Loaded extension {cog}')
            except commands.ExtensionNotFound:
                await ctx.send(f'There is no extension called {profanity.censor(cog)}')
            except commands.ExtensionAlreadyLoaded:
                await ctx.send('The extension is already loaded.')

    @commands.command(name='restart_cog', aliases=['reload_cog'], help='Restart a cog', hidden=True)
    async def restart_cog(self, ctx, cog):
        if ctx.author.id in database.get_owners_id():
            try:
                await self.bot.reload_extension(f'cogs.{cog}')
                await ctx.send(f"Successfully reloaded {cog}.")
            except commands.ExtensionNotFound:
                await ctx.send(f'There is no extension called {profanity.censor(cog)}')
            except commands.ExtensionFailed:
                await ctx.send('The extension failed.')


async def setup(bot):
    await bot.add_cog(Debug(bot))

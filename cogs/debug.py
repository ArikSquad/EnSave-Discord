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


class Debug(commands.Cog, description="Debugging"):
    EMOJI = "🔧"

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='admin', description="Admin debug", hidden=True)
    async def admin(self, ctx):
        if ctx.invoked_subcommand is None:
            if ctx.author.id in database.get_owner_ids():
                await ctx.send('Wow, an admin user!')

    @admin.command(name="profanity-test", aliases=["p-t"], hidden=True)
    async def profanity_test(self, ctx, *, text):
        if ctx.author.id in database.get_owner_ids():

            embed = discord.Embed(title="Profanity Test",
                                  description="Results of the debug profanity-test",
                                  color=0x00ff00)

            embed.add_field(name="Original", value=text)
            embed.add_field(name="Censored", value=profanity.censor(text))
            await ctx.send(embed=embed)

    @admin.command(name="eval", help="Evaluate code", hidden=True)
    async def eval(self, ctx, *, code):
        if ctx.author.id in database.get_owner_ids():
            try:
                result = eval(code)
                if result is not None:
                    await ctx.send(f"```py\n{result}```")
            except Exception as e:
                await ctx.send(f"```py\n{e}```")

    @admin.command(name="exec", help="Execute code", hidden=True)
    async def exec(self, ctx, *, code):
        if ctx.author.id in database.get_owner_ids():
            try:
                exec(code)
            except Exception as e:
                await ctx.send(f"```py\n{e}```")

    @admin.command(name="shutdown", help="Shutdown the bot.", aliases=["logout"], hidden=True)
    async def shutdown(self, ctx):
        if ctx.author.id in database.get_owner_ids():
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

    @admin.command(name='cog-unload', help='Unload a cog.', hidden=True)
    async def unload_cog(self, ctx, cog):
        if ctx.author.id in database.get_owner_ids():
            try:
                await self.bot.unload_extension(f'cogs.{cog}')
                await ctx.send(f"`{cog}` unloaded.")
                print(f"Unloaded extension {cog}")
            except commands.ExtensionNotFound:
                await ctx.send(f'There is no extension called {profanity.censor(cog)}')
            except commands.ExtensionNotLoaded:
                await ctx.send('The extension is already unloaded.')

    @admin.command(name='cog-load', help='Load a cog.', hidden=True)
    async def load_cog(self, ctx, cog):
        if ctx.author.id in database.get_owner_ids():
            try:
                await self.bot.load_extension(f'cogs.{cog}')
                await ctx.send(f'Loaded extension {cog}')
                print(f'Loaded extension {cog}')
            except commands.ExtensionNotFound:
                await ctx.send(f'There is no extension called {profanity.censor(cog)}')
            except commands.ExtensionAlreadyLoaded:
                await ctx.send('The extension is already loaded.')

    @admin.command(name='cog-restart', aliases=['cog-reload'], help='Restart a cog', hidden=True)
    async def restart_cog(self, ctx, cog):
        if ctx.author.id in database.get_owner_ids():
            try:
                await self.bot.reload_extension(f'cogs.{cog}')
                await ctx.send(f"Successfully reloaded {cog}.")
                print(f"Reloaded extension {cog}")
            except commands.ExtensionNotFound:
                await ctx.send(f'There is no extension called {profanity.censor(cog)}')
            except commands.ExtensionFailed:
                await ctx.send('The extension failed.')
            except commands.ExtensionNotLoaded:
                await ctx.send('The extension is not loaded.')


async def setup(bot):
    await bot.add_cog(Debug(bot))

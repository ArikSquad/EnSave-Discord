# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import json
import os

import nextcord
import nextcord.utils
from better_profanity import profanity
from nextcord.ext import commands

from utils import database


class Admin(commands.Cog, description="Gather information."):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", aliases=["information", "about"], help="Gather information about the bot.",
                      hidden=True)
    async def info(self, ctx, user: nextcord.User = None):
        if user is None and ctx.author.id in database.get_owners_id():
            embed = nextcord.Embed(title="Information", color=ctx.author.color)
            embed.add_field(name="Authors", value=str(database.get_owners_discord())[1:-1], inline=False)
            embed.add_field(name="Author IDs", value=str(database.get_owners_id())[1:-1], inline=False)
            embed.add_field(name="Library", value="nextcord")
            embed.add_field(name="Version", value=nextcord.__version__)
            embed.add_field(name="Guilds", value=len(self.bot.guilds))
            embed.add_field(name="Users", value=len(self.bot.users))
            embed.add_field(name="Latency", value=f"{self.bot.latency * 1000:.2f}ms")

            return await ctx.send(embed=embed)
        elif user is not None and ctx.author.id in database.get_owners_id():
            with open("db/users.json", "r") as f:
                data = json.load(f)
                exp = data[str(ctx.author.id)]['experience']
                level = data[str(ctx.author.id)]['level']
            embed = nextcord.Embed(title="Information", color=user.color)
            embed.set_thumbnail(url=user.avatar.url)
            embed.add_field(name="Username", value=user.name)
            embed.add_field(name="Tag", value=user.discriminator)
            embed.add_field(name="ID", value=user.id, inline=False)
            embed.add_field(name="Created at", value=user.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
            embed.add_field(name="Experience", value=exp if exp is not None else "None")
            embed.add_field(name="Level", value=level if level is not None else "None")
            embed.add_field(name="Premium", value="Yes" if database.get_premium(user.id) is True else "No",
                            inline=False)
            await ctx.send(embed=embed)

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
            sure = nextcord.Embed(title="Are you sure?", description="This will logout "
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
                self.bot.unload_extension(f'cogs.{cog}')
                await ctx.send(f"`{cog}` unloaded.")
            except commands.ExtensionNotFound:
                await ctx.send(f'There is no extension called {profanity.censor(cog)}')
            except commands.ExtensionNotLoaded:
                await ctx.send('The extension is already unloaded.')

    @commands.command(name='load_cog', help='Load a cog.', hidden=True)
    async def load_cog(self, ctx, cog):
        if ctx.author.id in database.get_owners_id():
            try:
                self.bot.load_extension(f'cogs.{cog}')
                await ctx.send(f'Loaded extension {profanity.censor(cog)}')
            except commands.ExtensionNotFound:
                await ctx.send(f'There is no extension called {profanity.censor(cog)}')
            except commands.ExtensionAlreadyLoaded:
                await ctx.send('The extension is already loaded.')

    @commands.command(name='restart_cog', aliases=['reload_cog'], help='Restart a cog', hidden=True)
    async def restart_cog(self, ctx, cog):
        if ctx.author.id in database.get_owners_id():
            try:
                self.bot.reload_extension(f'cogs.{cog}')
                await ctx.send(f"Successfully reloaded {cog}.")
            except commands.ExtensionNotFound:
                await ctx.send(f'There is no extension called {profanity.censor(cog)}')
            except commands.ExtensionFailed:
                await ctx.send('The extension failed.')

    @commands.command(name='restart_bot', help='Restart the bot.', hidden=True)
    async def restart_bot(self, ctx):
        if ctx.author.id in database.get_owners_id():
            view = database.YesNo()
            sure = nextcord.Embed(title="Are you sure?", description="This will restart the bot.",
                                  color=ctx.author.color)
            message = await ctx.send(embed=sure, view=view)
            await view.wait()
            if view.value is None:
                return
            elif view.value:
                await message.delete()
                await self.bot.close()
                os.system("python3 main.py")

    @commands.command(name='set_premium', help='Set premium state of a user.', hidden=True)
    async def set_premium(self, ctx, user: nextcord.Member, state: bool = True):
        if ctx.author.id in database.get_owners_id():
            database.set_premium(user.id, state)
            await ctx.send(f"{user.mention} is now a premium user.")


def setup(bot):
    bot.add_cog(Admin(bot))

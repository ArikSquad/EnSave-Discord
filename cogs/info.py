# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import json

import nextcord
import nextcord.utils
from better_profanity import profanity
from nextcord.ext import commands

from utils import database


class Info(commands.Cog, description="Gather information."):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id == self.bot.user.id:
            return
        # Write the username to the user.json.
        with open('db/users.json', 'r+') as f:
            data = json.load(f)
            # Check if the username is in the file inside message.author.id
            if str(message.author.id) not in data:
                data[str(message.author.id)]['username'] = str(message.author.name)
                json.dump(data, f, indent=4)

    @commands.command(name="info", aliases=["information", "about"], help="Gather information about the bot.",
                      hidden=True)
    async def info(self, ctx, user: nextcord.User = None):
        if user is None and ctx.author.id in database.get_owner_ids():
            embed = nextcord.Embed(title="Information", color=ctx.author.color)
            embed.add_field(name="Author", value="ArikSquad#6222")
            embed.add_field(name="Library", value="nextcord")
            embed.add_field(name="Version", value=nextcord.__version__)
            embed.add_field(name="Guilds", value=len(self.bot.guilds))
            embed.add_field(name="Users", value=len(self.bot.users))
            embed.add_field(name="Latency", value=f"{self.bot.latency * 1000:.2f}ms")

            return await ctx.send(embed=embed)
        elif user is not None and ctx.author.id in database.get_owner_ids():
            with open("db/users.json", "r") as f:
                data = json.load(f)
                if user.id in data:
                    exp = data[str(ctx.author.id)]['experience']
                    level = data[str(ctx.author.id)]['level']
            embed = nextcord.Embed(title="Information", color=ctx.author.color)
            embed.set_thumbnail(url=user.avatar.url)
            embed.set_image(url=user.banner.url)
            embed.add_field(name="Username", value=user.name)
            embed.add_field(name="Discriminator", value=user.discriminator)
            embed.add_field(name="ID", value=user.id)
            embed.add_field(name="Created at", value=user.created_at.strftime("%d/%m/%Y %H:%M:%S"))
            embed.add_field(name="Color", value=f"{user.color.value:0>6x}")
            embed.add_field(name="Experience", value=exp if exp is not None else "None")
            embed.add_field(name="Level", value=level if level is not None else "None")
            embed.add_field(name="Premium", value="Yes" if database.get_premium(user.id) is True else "No")

    @commands.command(name="eval", help="Evaluate code", hidden=True)
    async def eval(self, ctx, *, code):
        if ctx.author.id in database.get_owner_ids():
            try:
                result = eval(code)
                if result is not None:
                    await ctx.send(f"```py\n{result}```")
            except Exception as e:
                await ctx.send(f"```py\n{e}```")

    @commands.command(name="exec", help="Execute code", hidden=True)
    async def exec(self, ctx, *, code):
        if ctx.author.id in database.get_owner_ids():
            try:
                exec(code)
            except Exception as e:
                await ctx.send(f"```py\n{e}```")

    @commands.command(name="shutdown", help="Shutdown the bot.", hidden=True)
    async def shutdown(self, ctx):
        if ctx.author.id in database.get_owner_ids():
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
        if ctx.author.id in database.get_owner_ids():
            try:
                self.bot.unload_extension(f'cogs.{cog}')
                await ctx.send(f"`{cog}` unloaded.")
            except commands.ExtensionNotFound:
                await ctx.send(f'There is no extension called {profanity.censor(cog)}')
            except commands.ExtensionNotLoaded:
                await ctx.send('The extension is already unloaded.')

    @commands.command(name='load_cog', help='Load a cog.', hidden=True)
    async def load_cog(self, ctx, cog):
        if ctx.author.id in database.get_owner_ids():
            try:
                self.bot.load_extension(f'cogs.{cog}')
                await ctx.send(f'Loaded extension {profanity.censor(cog)}')
            except commands.ExtensionNotFound:
                await ctx.send(f'There is no extension called {profanity.censor(cog)}')
            except commands.ExtensionAlreadyLoaded:
                await ctx.send('The extension is already loaded.')

    @commands.command(name='restart_cog', help='Restart a cog', hidden=True)
    async def restart_cog(self, ctx, cog):
        if ctx.author.id in database.get_owner_ids():
            try:
                self.bot.reload_extension(f'cogs.{cog}')
                await ctx.send(f"Successfully reloaded {cog}.")
            except commands.ExtensionNotFound:
                await ctx.send(f'There is no extension called {profanity.censor(cog)}')
            except commands.ExtensionFailed:
                await ctx.send('The extension failed.')

    @commands.command(name='add_premium', help='Add a premium user', hidden=True)
    async def add_premium(self, ctx, user: nextcord.Member):
        if ctx.author.id in database.get_owner_ids():
            database.set_premium(user.id, True)
            await ctx.send(f"{user.mention} is now a premium user.")


def setup(bot):
    bot.add_cog(Info(bot))

# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import json

import discord
import psutil as psutil
from better_profanity import profanity
from discord.ext import commands

from utils import database, buttons


class Admin(commands.Cog, description="Gather information"):
    EMOJI = "📜"

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='admin', help="Admin commands for debugging", hidden=True,
                    brief='Debugging the features of the bot')
    async def admin(self, ctx):
        if ctx.invoked_subcommand is None:
            if ctx.author.id in database.get_owner_ids():
                await ctx.send('Wow, an admin user!')

    @admin.command(name="profanity-test", aliases=["p-t"], hidden=True,
                   help="Test the profanity filter used in some commands",
                   brief="Profanity filter tester")
    async def profanity_test(self, ctx, *, text):
        if ctx.author.id in database.get_owner_ids():
            embed = discord.Embed(title="Profanity Test",
                                  description="Results of the debug profanity-test",
                                  color=0x00ff00)

            embed.add_field(name="Original", value=text)
            embed.add_field(name="Censored", value=profanity.censor(text))
            await ctx.send(embed=embed)

    @admin.command(name="exec", help="Executing code using python eval", hidden=True,
                   brief="Try python code")
    async def exec(self, ctx, *, code):
        if ctx.author.id in database.get_owner_ids():
            try:
                exec(code)
            except Exception as e:
                await ctx.send(f"```py\n{e}```")

    @admin.command(name="shutdown", help="Logout from discord.", aliases=["logout"], hidden=True,
                   brief="Close connection to discord")
    async def shutdown(self, ctx):
        if ctx.author.id in database.get_owner_ids():
            view = buttons.YesNo()
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

    @admin.command(name='cog-unload', help='Unload a cog.', hidden=True,
                   brief='Disable a cog.')
    async def unload_cog(self, ctx, cog):
        if ctx.author.id in database.get_owner_ids():
            try:
                await self.bot.unload_extension(f'cogs.{cog}')
                await ctx.send(f"`{cog}` unloaded.")
                print(f"Unloaded extension {cog}")
            except commands.ExtensionNotFound:
                await ctx.send(f'There is no extension called {profanity.censor(cog)}')

    @admin.command(name='cog-load', help='Load a cog.', hidden=True,
                   brief='Enable a cog.')
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

    @admin.command(name='cog-restart', aliases=['cog-reload'], help='Restart a cog', hidden=True,
                   brief='Reload a cog.')
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

    @admin.command(name="info", aliases=["information", "about"], help="Gather information about the bot.",
                   hidden=True, brief='See information about bot or a user')
    async def info(self, ctx, user: discord.User = None):
        if user is None and ctx.author.id in database.get_owner_ids():
            embed = discord.Embed(title="Information", color=ctx.author.color)
            embed.add_field(name="Authors", value=str(database.get_owners_discord())[1:-1], inline=False)
            embed.add_field(name="Author IDs", value=str(database.get_owner_ids())[1:-1], inline=False)
            embed.add_field(name="Library", value="discord")
            embed.add_field(name="Version", value=discord.__version__)
            embed.add_field(name="Guilds", value=len(self.bot.guilds))
            embed.add_field(name="Users", value=len(self.bot.users))
            embed.add_field(name="Latency", value=f"{self.bot.latency * 1000:.2f}ms")
            embed.add_field(name="Memory", value=str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB",
                            inline=False)
            embed.add_field(name="OS Last Boot", value=f"{psutil.boot_time()}")
            embed.add_field(name="CPU Percentage", value=f"{psutil.cpu_percent()}%")
            return await ctx.send(embed=embed)
        elif user is not None and ctx.author.id in database.get_owner_ids():
            with open("db/users.json", "r") as f:
                data = json.load(f)
                exp = data[str(ctx.author.id)]['experience']
                level = data[str(ctx.author.id)]['level']
            embed = discord.Embed(title="Information", color=user.color)
            embed.set_thumbnail(url=user.avatar.url)
            embed.add_field(name="Username", value=user.name)
            embed.add_field(name="Discriminator", value=user.discriminator, inline=False)
            embed.add_field(name="ID", value=user.id, inline=False)
            embed.add_field(name="Created at", value=user.created_at.strftime("%d/%m/%Y %H:%M:%S"), inline=False)
            embed.add_field(name="Experience", value=exp if exp is not None else "None")
            embed.add_field(name="Level", value=level if level is not None else "None")
            embed.add_field(name="Premium", value="Yes" if database.get_premium(user.id) is True else "No",
                            inline=False)
            embed.add_field(name="Bot Status", value="Yes" if user.bot is True else "No", inline=False)
            embed.add_field(name="Bot Owner", value="Yes" if user.id in database.get_owner_ids() else "No",
                            inline=False)
            await ctx.send(embed=embed)

    @admin.command(name='set-premium', help='Set premium state of a user.', hidden=True,
                   brief='Change user premium state')
    async def set_premium(self, ctx, user: discord.Member, state: bool = None):
        if ctx.author.id in database.get_owner_ids():
            if user.id in database.get_owner_ids():
                await ctx.send("You can't set the premium state of an owner.")
            else:
                if state:
                    database.set_premium(user.id, state)
                else:
                    database.set_premium(user.id)
                await ctx.send(f"{user.mention}'s new state of premium: {state}")


async def setup(bot):
    await bot.add_cog(Admin(bot))

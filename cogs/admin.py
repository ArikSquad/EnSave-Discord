# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import datetime
import json
import platform

import discord
import psutil as psutil
from better_profanity import profanity
from discord.ext import commands

from utils import database


class Admin(commands.Cog, description="Gather information."):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="info", aliases=["information", "about"], help="Gather information about the bot.",
                      hidden=True)
    async def info(self, ctx, user: discord.User = None):
        if user is None and ctx.author.id in database.get_owners_id():
            embed = discord.Embed(title="Information", color=ctx.author.color)
            embed.add_field(name="Authors", value=str(database.get_owners_discord())[1:-1], inline=False)
            embed.add_field(name="Author IDs", value=str(database.get_owners_id())[1:-1], inline=False)
            embed.add_field(name="Library", value="discord")
            embed.add_field(name="Version", value=discord.__version__)
            embed.add_field(name="Guilds", value=len(self.bot.guilds))
            embed.add_field(name="Users", value=len(self.bot.users))
            embed.add_field(name="Latency", value=f"{self.bot.latency * 1000:.2f}ms")
            embed.add_field(name="Python", value=f"{platform.python_version()}")
            embed.add_field(name="Operating System", value=f"{platform.system()}", inline=False)
            embed.add_field(name="Processor", value=f"{platform.processor()}", inline=False)
            embed.add_field(name="Memory", value=str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB",
                            inline=False)
            embed.add_field(name="OS Last Boot", value=f"{psutil.boot_time()}")
            embed.add_field(name="Bit Version", value=f"{platform.machine()}")
            embed.add_field(name="CPU Percentage", value=f"{psutil.cpu_percent()}%")
            return await ctx.send(embed=embed)
        elif user is not None and ctx.author.id in database.get_owners_id():
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
            embed.add_field(name="Bot Owner", value="Yes" if user.id in database.get_owners_id() else "No",
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

    @commands.command(name='set_premium', help='Set premium state of a user.', hidden=True)
    async def set_premium(self, ctx, user: discord.Member, state: bool = None):
        if ctx.author.id in database.get_owners_id():
            if user.id in database.get_owners_id():
                await ctx.send("You can't set the premium state of an owner.")
            else:
                if state:
                    database.set_premium(user.id, state)
                else:
                    database.set_premium(user.id)
                await ctx.send(f"{user.mention}'s new state of premium: {state}")

    # This command has been forked from
    # https://github.com/Carberra/updated-discord.py-tutorial/blob/085113e9bff69a699a25ed1cd91db5744b8755ea/lib/cogs/info.py#L37
    @commands.command(name="serverinfo", aliases=["guildinfo", "si", "gi"])
    @commands.has_permissions(administrator=True)
    async def server_info(self, ctx):
        embed = discord.Embed(title="Server information",
                              colour=ctx.guild.owner.colour,
                              timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url=ctx.guild.icon.url)

        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        fields = [("ID", ctx.guild.id, True),
                  ("Owner", ctx.guild.owner, True),
                  ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Members", len(ctx.guild.members), True),
                  ("Users", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                  ("Banned members", len(await ctx.guild.bans()), True),
                  ("Statuses", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
                  ("Text channels", len(ctx.guild.text_channels), True),
                  ("Voice channels", len(ctx.guild.voice_channels), True),
                  ("Categories", len(ctx.guild.categories), True),
                  ("Roles", len(ctx.guild.roles), True),
                  ("Invites", len(await ctx.guild.invites()), True),
                  ("\u200b", "\u200b", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    # The administrators command to change the prefix of the bot.
    @commands.command(name="prefix", help="Change the prefix of the guild.",
                      aliases=["changeprefix"])
    @commands.has_permissions(administrator=True)
    async def change_prefix(self, ctx, prefix):
        embed = discord.Embed(title="Moderation",
                              description=f"Changed the prefix to: " + prefix,
                              color=discord.Color.gold())
        await ctx.send(embed=embed)

        # Opens the prefixes.json to read the prefixes.
        with open('db/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix

        # Writes the prefixes back to the file
        with open('db/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        print(f'Changed prefix in {ctx.guild} to {prefix}. Command was ran user {ctx.message.author}.')


async def setup(bot):
    await bot.add_cog(Admin(bot))

# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2021-2022 MikArt
# Released under the Apache License 2.0
#
# -----------------------------------------------------------
import asyncio
import random
import string
import time as tm
import typing
from datetime import datetime, timedelta

import aiohttp
import discord
import psutil as psutil
from discord import app_commands
from discord.ext import commands

from utils import utility, db


# noinspection PyUnusedLocal
class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None
        self.response = None

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        await self.response.edit(view=self)

    @discord.ui.button(label='Confirm', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Confirming', ephemeral=True)
        self.value = True
        self.stop()

    @discord.ui.button(label='Cancel', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('Cancelling', ephemeral=True)
        self.value = False
        self.stop()


# Convert input to time. example: 1h = 3600
def convert(time):
    pos = ["s", "m", "h", "d"]

    time_dict = {"s": 1, "m": 60, "h": 3600, "d": 3600 * 24}

    unit = time[-1]

    if unit not in pos:
        return -1
    try:
        val = int(time[:-1])
    except ValueError:
        return -2

    return val * time_dict[unit]


# Get a randomized string
def get_string():
    letters = ''.join((random.choice(string.ascii_letters) for _ in range(8)))
    digits = ''.join((random.choice(string.digits) for _ in range(4)))
    sample_list = list(letters + digits)
    random.shuffle(sample_list)
    final_string = ''.join(sample_list)
    return "a" + final_string


class Admin(commands.Cog, description="Administration commands for the bot"):
    group = app_commands.Group(name="admin", description="Administration commands for EnSave",
                               guild_ids=[988505821472247919])

    def __init__(self, bot):
        self.bot = bot

    @group.command(name="shutdown", description="Logout from discord")
    async def shutdown(self, interaction: discord.Interaction):
        if interaction.user.id in utility.get_owner():
            view = Confirm()
            sure = discord.Embed(title="Are you sure?", description="This will logout "
                                                                    "from discord and exit the python program.",
                                 color=discord.Color.from_rgb(48, 50, 54))
            message = await interaction.response.send_message(embed=sure, view=view)
            await view.wait()
            if view.value is None:
                return
            elif view.value:
                await message.delete()
                await self.bot.close()

    @group.command(name='unload-cog', description='Unload a cog.')
    async def unload_cog(self, interaction: discord.Interaction, cog: str):
        if interaction.user.id in utility.get_owner():
            try:
                await self.bot.unload_extension(f'cogs.{cog.lower()}')
                await interaction.response.send_message(f"Unloaded `{cog}`.")
                print(f"Unloaded extension {cog}")
            except commands.ExtensionNotLoaded:
                await interaction.response.send_message(f'The extension {cog} '
                                                        f'is not loaded or has not been found.')

    @group.command(name='load-cog', description='Load a cog.')
    async def load_cog(self, interaction: discord.Interaction, cog: str):
        if interaction.user.id in utility.get_owner():
            try:
                await self.bot.load_extension(f'cogs.{cog.lower()}')
                await interaction.response.send_message(f'Loaded `{cog}`.')
                print(f'Loaded extension {cog}')
            except commands.ExtensionNotFound:
                await interaction.response.send_message(f'There is no extension called {cog}')
            except commands.ExtensionAlreadyLoaded:
                await interaction.response.send_message('The extension is already loaded.')

    @group.command(name='restart-cog', description='Restart a cog')
    async def restart_cog(self, interaction: discord.Interaction, cog: str):
        if interaction.user.id in utility.get_owner():
            try:
                await self.bot.unload_extension(f'cogs.{cog.lower()}')
                await self.bot.load_extension(f'cogs.{cog.lower()}')
                await interaction.response.send_message(f"Reloaded `{cog}`.")
                print(f"Reloaded extension {cog}")
            except commands.ExtensionFailed:
                await interaction.response.send_message('The extension failed.')
            except commands.ExtensionNotLoaded:
                await interaction.response.send_message('The extension is not loaded or has not been found.')

    @group.command(name="info", description="Gather information about the bot.")
    @app_commands.guild_only()
    async def info(self, interaction: discord.Interaction, user: discord.Member = None):
        if not user and interaction.user.id in utility.get_owner():
            embed = discord.Embed(title="Information", color=discord.Color.from_rgb(48, 50, 54))
            embed.add_field(name="Authors", value=str(utility.get_owner())[1:-1], inline=False)
            embed.add_field(name="Author IDs", value=str(utility.get_owner())[1:-1], inline=False)
            embed.add_field(name="Library", value=f"{discord.__title__} by {discord.__author__}")
            embed.add_field(name="Version", value=discord.__version__)
            embed.add_field(name="Guilds", value=len(self.bot.guilds))
            embed.add_field(name="Users", value=len(self.bot.users))
            embed.add_field(name="Latency", value=f"{self.bot.latency * 1000:.2f}ms")
            embed.add_field(name="Memory", value=str(round(psutil.virtual_memory().total /
                                                           (1024.0 ** 3))) + " GB",
                            inline=False)
            embed.add_field(name="OS Last Boot", value=f"{psutil.boot_time()}")
            embed.add_field(name="CPU Percentage", value=f"{psutil.cpu_percent()}%")
            await interaction.response.send_message(embed=embed)
        else:
            if user and interaction.user.id in utility.get_owner():
                embed = discord.Embed(title="Information", color=discord.Color.from_rgb(48, 50, 54))
                embed.set_thumbnail(url=user.avatar.url)
                embed.add_field(name="Username", value=user.name)
                embed.add_field(name="Discriminator", value=user.discriminator, inline=False)
                embed.add_field(name="ID", value=user.id, inline=False)
                embed.add_field(name="Created at", value=user.created_at.strftime("%d/%m/%Y %H:%M:%S"),
                                inline=False)
                embed.add_field(name="Premium", value="Yes" if db.get_user_premium(user.id) is True else "No",
                                inline=False)
                embed.add_field(name="Bot Status", value="Yes" if user.bot is True else "No", inline=False)
                embed.add_field(name="Bot Owner", value="Yes" if user.id in utility.get_owner() else "No",
                                inline=False)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("You do not have permissions.")

    @group.command(name='set-premium', description='Set premium state of a user.')
    async def set_premium(self, interaction: discord.Interaction, user: discord.Member, state: bool = None):
        if interaction.user.id in utility.get_owner():
            if state:
                utility.set_premium(user.id, state)
            else:
                utility.set_premium(user.id)
            await interaction.response.send_message(f"{user.mention}'s new state of premium: {state}")

    @group.command(name='get-premium', description='Get premium state of a user.')
    async def get_premium(self, interaction: discord.Interaction, user: discord.Member):
        if interaction.user.id in utility.get_owner():
            await interaction.response.send_message(f"{user.mention}'s premium state: {db.get_user_premium(user.id)}")

    @group.command(name="message", description="Send an group message to a user.")
    async def message(self, interaction: discord.Interaction, user: discord.Member, message: str):
        if interaction.user.id in utility.get_owner():
            await user.send(message)

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, guilds: commands.Greedy[discord.Object],
                   spec: typing.Optional[typing.Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "*":
                ctx.bot.tree.copy_global_to(guild=ctx.guild)
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
            elif spec == "^":
                ctx.bot.tree.clear_commands(guild=ctx.guild)
                await ctx.bot.tree.sync(guild=ctx.guild)
                synced = []
            else:
                synced = await ctx.bot.tree.sync()

            await ctx.send(
                f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1

        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

    @app_commands.command(name='keydrop', description='Drop a key.')
    @app_commands.guild_only()
    async def keydrop(self, interaction: discord.Interaction, time: str = "1m", key: str = None):
        if interaction.user.id in utility.get_owner():
            if not str(key).startswith("a"):
                await interaction.message.delete()

            key = key if key else get_string()

            # Create the embed and convert the wait time to seconds
            embed = discord.Embed(title="Key", color=discord.Color.from_rgb(48, 50, 54), timestamp=datetime.utcnow())
            wait = convert(time)

            # Send the message
            formatted_time = datetime.utcnow() + timedelta(seconds=wait)
            unix_time = tm.mktime(formatted_time.timetuple())
            embed.add_field(name="Key drop!", value=f"Coming at <t:{int(unix_time)}:T>", inline=False)
            embed.add_field(name="How to redeem?", value=f"Use `/redeem <key>`", inline=False)
            embed.set_footer(text=f"Created by {interaction.user.name}")
            message = await interaction.response.send_message(embed=embed)

            db.add_code(key)

            # Waiting for the converted time.
            await asyncio.sleep(wait)
            # Change the field to show the code
            embed.set_field_at(0, name="Key Drop!", value=f"{key}")
            await message.edit(embed=embed)
        else:
            await interaction.response.send_message("This command is for the supreme leader of the bot.",
                                                    ephemeral=True)

    @group.command(name='webhook', description='Send a message through webhooks.')
    @app_commands.guild_only()
    async def webhook(self, interaction: discord.Interaction, url: str, message: str, username: str = "EnSave"):
        if interaction.user.id in utility.get_owner():
            async with aiohttp.ClientSession() as session:
                webhook: discord.Webhook = discord.Webhook.from_url(url, session=session)
                avatar = interaction.user.avatar.url
                await webhook.send(message, username=username,
                                   avatar_url=avatar if avatar else self.bot.user.avatar.url)
            await interaction.response.send_message("Message sent.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Admin(bot))

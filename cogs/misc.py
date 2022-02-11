# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

import os
import secrets
import time

import aiohttp
import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext, MenuContext, ContextMenuType
from dotenv import load_dotenv

from utils import getter

guild_ids = [770634445370687519]
load_dotenv()
secret = os.getenv('discord_secret')


class Misc(commands.Cog, description="Slash Commands"):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="dog", guild_ids=guild_ids, description="Dog pictures!")
    async def dog(self, ctx: SlashContext):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://random.dog/woof.json") as r:
                data = await r.json()
                embed = discord.Embed(
                    title="Doggo",
                    color=ctx.author.color
                )
                embed.set_image(url=data['url'])
                await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="Password", guild_ids=guild_ids)
    async def password(self, ctx, letters: int = 18):
        """ Generates a random password string for you containing nbytes random bytes.
        """

        embed1 = discord.Embed(title=f"Misc", description="I only accept any numbers between 3-1400",
                               color=discord.Color.dark_red())

        embed2 = discord.Embed(title=f"Misc", description=f"Sending you a private message with your "
                                                          f"random generated password **{ctx.author.name}**",
                               color=discord.Color.green())

        embed3 = discord.Embed(title=f"Misc", description=f"🎁 **Here is your "
                                                          f"password:**\n{secrets.token_urlsafe(letters)}",
                               color=discord.Color.green())

        if letters not in range(3, 1401):
            return await ctx.send(embed=embed1)
        if hasattr(ctx, "guild") and ctx.guild is not None:
            await ctx.reply(embed=embed2)
        await ctx.author.send(embed=embed3)

    @cog_ext.cog_context_menu(target=ContextMenuType.MESSAGE, name='Resend', guild_ids=guild_ids)
    async def _resend(self, ctx: MenuContext):
        await ctx.send(f"{ctx.target_message.author}: **{ctx.target_message.content}**")

    @cog_ext.cog_slash(name='Say', guild_ids=guild_ids)
    async def say(self, ctx, *, text):
        """Says what you want it to say"""
        msg = discord.Embed(description=text,
                            color=ctx.author.color,
                            timestamp=getter.get_time()
                            )
        await ctx.send(embed=msg)

    @cog_ext.cog_slash(name="Invite", guild_ids=guild_ids)
    async def _invite(self, ctx):
        """
        Get the invite link of the bot.
        """
        embed = discord.Embed(
            title="Info",
            description=f"Invite me by clicking"
                        f" [here](https://discord.com/api/oauth2/authorize?"
                        f"client_id=812808865728954399&permissions=8&redirect_uri="
                        f"http%3A%2F%2Fdiscord.mikart.eu%2F&scope=bot%20applications.commands).",
            color=0xD75BF4
        )
        await ctx.author.send(embed=embed)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="Latency", guild_ids=guild_ids)
    async def _latency(self, ctx):
        """Shows the latency of the bot."""
        wait = discord.Embed(title="Info",
                             description=f"Waiting the server to respond!",
                             color=ctx.author.color)

        before = time.monotonic()
        message = await ctx.send(embed=wait)
        ping = (time.monotonic() - before) * 1000

        waited = discord.Embed(title="Info",
                               description=f"Pong!  `{int(ping)}ms`",
                               color=ctx.author.color)
        await message.edit(embed=waited)
        print(f'Ping {int(ping)}ms')

    @cog_ext.cog_slash(name="Server", guild_ids=guild_ids)
    async def _server(self, ctx):
        """ Get an invitation to our support server! """

        embed = discord.Embed(title="Info",
                              description=f"**Here you go {ctx.author.name} 🍻**\n[Click Me](http://discord.mikart.eu/)",
                              color=discord.Color.green())

        embed2 = discord.Embed(title="Info",
                               description=f"**{ctx.author.name}** This is the support server!",
                               color=ctx.author.color)

        if isinstance(ctx.channel, discord.DMChannel) or ctx.guild.id != 770634445370687519:
            return await ctx.send(embed=embed)
        await ctx.send(embed=embed2)

    @cog_ext.cog_slash(name="GitHub", guild_ids=guild_ids)
    async def _github(self, ctx):
        """Returns a link for the GitHub"""
        embed1 = discord.Embed(title=f"Misc",
                               description="Check the code from [Click Me]"
                                           "(https://github.com/ariksquad/ensave-discord)",
                               color=ctx.author.color)
        await ctx.send(embed=embed1)

    @cog_ext.cog_slash(name="Avatar", guild_ids=guild_ids)
    async def avatar(self, ctx, *, member: discord.Member = None):
        """Returns select user's avatar"""
        if not member:
            member = ctx.message.author

        embed = discord.Embed(
            title=member.display_name,
            color=member.color
        )
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="clear", guild_ids=guild_ids, description="Purge commands")
    @commands.has_permissions(manage_messages=True, manage_channels=True)
    async def clear(self, ctx, amount):
        """
        Delete a number of messages.
        """
        try:
            amount = int(amount)
        except ValueError:
            embed = discord.Embed(
                title="Error!",
                description=f"`{amount}` is not a valid number.",
                color=0xE02B2B
            )
            await ctx.send(embed=embed)
            return
        if amount < 1:
            embed = discord.Embed(
                title="Error!",
                description=f"`{amount}` is not a valid number.",
                color=0xE02B2B
            )
            await ctx.send(embed=embed)
            return
        purged_messages = await ctx.message.channel.purge(limit=amount)
        embed = discord.Embed(
            title="Chat Cleared!",
            description=f"**{ctx.message.author}** cleared **{len(purged_messages)}** messages!",
            color=0x42F56C
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))

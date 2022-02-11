# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2021 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

import asyncio
import datetime
import os
import random
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


class Slash(commands.Cog, description="Slash Commands"):
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

    @cog_ext.cog_slash(name="rps", guild_ids=guild_ids, description="Rock? Paper? Scissors!")
    async def rps(self, ctx):
        def check_win(p, b):
            if p == '🌑':
                return False if b == '📄' else True
            if p == '📄':
                return False if b == '✂' else True
            return False if b == '🪨' else True

        async with ctx.typing():
            reactions = ['🪨', '📄', '✂']
            game_message = await ctx.send("**Rock Paper Scissors**\nChoose your shape:", delete_after=15.0)
            for reaction in reactions:
                await game_message.add_reaction(reaction)
            bot_emoji = random.choice(reactions)

        def check(reaction2s, user):
            return user != self.bot.user and user == ctx.author and (str(reaction2s.emoji) == '🪨' or '📄' or '✂')

        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=10.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("Time's Up! :stopwatch:")
        else:
            await ctx.send(f"**YOU:\t{reaction.emoji}\nME:\t{bot_emoji}**")
            if str(reaction.emoji) == bot_emoji:
                embed1 = discord.Embed(title=f"Games", description="**It's a Tie :ribbon:**",
                                       color=discord.Color.gold())
                await ctx.send(embed=embed1)
            elif check_win(str(reaction.emoji), bot_emoji):
                embed2 = discord.Embed(title=f"Games", description="**You win :sparkles:**",
                                       color=discord.Color.green())
                await ctx.send(embed=embed2)
            else:
                embed3 = discord.Embed(title=f"Games", description="**I win :robot:**",
                                       color=discord.Color.red())
                await ctx.send(embed=embed3)

    @cog_ext.cog_slash(name="cookie", guild_ids=guild_ids, description="Cookie game!")
    async def cookie(self, ctx):
        """Who can catch the cookie first?"""

        m = await ctx.send(embed=discord.Embed(title="🍪 Cookie is coming..."))
        await asyncio.sleep(3)

        for i in range(3, 0, -1):
            await m.edit(embed=discord.Embed(title=f"🍪 Cookie is coming in **{i}**"))
            await asyncio.sleep(1)

        start = datetime.datetime.now()
        await m.add_reaction("🍪")
        try:
            _, user = await self.bot.wait_for(
                "reaction_add",
                check=lambda r, u: str(r.emoji) == "🍪" and r.message == m and not u.bot,
                timeout=10,
            )
        except asyncio.TimeoutError:
            prank = await ctx.send("No one got the cookie :(")
            await asyncio.sleep(2)
            prank.edit(content="Just kidding, you got the cookie! :)")
        else:
            time_variable = round((datetime.datetime.utcnow() - start).total_seconds() - self.bot.latency, 3)
            await m.edit(embed=discord.Embed(
                title=f"**{user.display_name}** got the cookie in **{time_variable}** seconds")
            )

    @cog_ext.cog_slash(name="8ball", guild_ids=guild_ids)
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def eightball(self, ctx, *, question: commands.clean_content):
        """ Consult 8ball to receive an answer """
        ballresponse = [
            "Yes", "No", "Take a wild guess...", "Very doubtful",
            "Sure", "Without a doubt", "Most likely", "Might be possible",
            "You'll be the judge", "no... (╯°□°）╯︵ ┻━┻", "no... baka",
            "senpai, pls no ;-;", "I have no idea"
        ]

        answer = random.choice(ballresponse)

        embed1 = discord.Embed(title=f"{question}", description=f":8ball: {answer}",
                               color=ctx.author.color)

        await ctx.send(embed=embed1)

    @cog_ext.cog_slash(name="Slot", guild_ids=guild_ids)
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        embed1 = discord.Embed(title=f"Games", description=f"{slotmachine} All matching, you won! 🎉",
                               color=discord.Color.green())
        embed2 = discord.Embed(title=f"Games", description=f"{slotmachine} 2 in a row, you won! 🎉",
                               color=discord.Color.purple())
        embed3 = discord.Embed(title=f"Games", description=f"{slotmachine} No match, you lost 😢",
                               color=discord.Color.red())

        if a == b == c:
            await ctx.send(embed=embed1)
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(embed=embed2)
        else:
            await ctx.send(embed=embed3)

    @cog_ext.cog_context_menu(target=ContextMenuType.MESSAGE, name='Resend', guild_ids=guild_ids)
    async def test(self, ctx: MenuContext):
        await ctx.send(f"{ctx.target_message.author}: **{ctx.target_message.content}**")

    @cog_ext.cog_slash(name='Say', guild_ids=guild_ids)
    async def say(self, ctx, *, text):
        """Says what you want it to say"""
        msg = discord.Embed(description=text,
                            color=ctx.author.color,
                            timestamp=getter.get_timestamp()
                            )
        await ctx.send(embed=msg)

    @cog_ext.cog_slash(name="Invite", guild_ids=guild_ids)
    async def invite(self, ctx):
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

    @cog_ext.cog_slash(name="Dice", guild_ids=guild_ids)
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def _dice(self, ctx):
        """Roll dice!"""
        embed1 = discord.Embed(title=f"Games", description="Rolled a {}!".format(random.randint(1, 6)),
                               color=discord.Color.green())
        await ctx.send(embed=embed1)

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

    @cog_ext.cog_slash(name="Slap", guild_ids=guild_ids)
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def slap(self, ctx, member: discord.User = None):
        """Slaps someone you select"""
        emb = discord.Embed(title="Games",
                            description=f"{ctx.message.author.mention} slaps {member.mention} in the face!",
                            color=0x3498db)

        await ctx.send(embed=emb)

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

    # a slash command for coinflip
    @cog_ext.cog_slash(name="Coinflip", guild_ids=guild_ids)
    async def coinflip(self, ctx):
        """Flips a coin"""

        determine_flip = [1, 0]
        if random.choice(determine_flip) == 1:
            embed = discord.Embed(title="Fun",
                                  description=f"{ctx.author.mention} Flipped coin, we got **Heads**!",
                                  color=ctx.author.color)
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title="Fun",
                                  description=f"{ctx.author.mention} Flipped coin, we got **Tails**!",
                                  color=ctx.author.color)
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
    bot.add_cog(Slash(bot))

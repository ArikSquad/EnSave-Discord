import discord
import random
from discord.ext import commands
import aiohttp
import time
import asyncio


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(help="Says something what you like.", brief="Says something after the command")
    async def say(self, ctx, *, text):
        msg = discord.Embed(title="Fun",
                            description=f'' + ctx.message.author.mention + ': ' + text,
                            color=discord.Color.green())
        async with ctx.typing():
            await asyncio.sleep(2)
        await ctx.send(embed=msg)

    @commands.command(help="Says hello to you!", brief="Says a nice little hello back to you.")
    async def hello(self, ctx):
        msg = discord.Embed(title="Fun",
                            description=f"Hello {ctx.author.name}",
                            color=discord.Color.green())
        await ctx.send(embed=msg)

    @commands.command(name="invite")
    async def invite(self, context):
        """
        Get the invite link of the bot to be able to invite it.
        """
        embed = discord.Embed(
            description=f"Invite me by clicking [here](https://discord.com/api/oauth2/authorize?client_id=812808865728954399&permissions=8&redirect_uri=http%3A%2F%2Fdiscord.mikart.eu%2F&scope=bot%20applications.commands).",
            color=0xD75BF4
        )
        try:
            # To know what permissions to give to your bot, please see here: https://discordapi.com/permissions.html and remember to not give Administrator permissions.
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.command(help="Prints the User pfp.", brief="Prints the User profile picture.")
    async def user(self, ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.message.author

        a = member.avatar_url
        ctx.send(a)

    @commands.command(pass_context=True, help="Shows the latency.", brief="Shows the latency.")
    async def ping(self, ctx):
        wait = discord.Embed(title="Fun",
                             description=f"Waiting the server to respond!",
                             color=discord.Color.red())

        before = time.monotonic()
        message = await ctx.send(embed=wait)
        ping = (time.monotonic() - before) * 1000

        waited = discord.Embed(title="Fun",
                               description=f"Pong!  `{int(ping)}ms`",
                               color=discord.Color.green())
        await message.edit(embed=waited)
        print(f'Ping {int(ping)}ms')

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def slap(self, ctx, member: discord.User = None):
        emb = discord.Embed(title=None,
                            description=f"{ctx.message.author.mention} slaps {member.mention} in the face!",
                            color=0x3498db)

        await ctx.send(embed=emb)

    @commands.command()
    async def dog(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://random.dog/woof.json") as r:
                data = await r.json()
                embed = discord.Embed(
                    title="Doggo",
                    color=ctx.author.color
                )
                embed.set_image(url=data['url'])

                await ctx.send(embed=embed)

    # Meme command
    @commands.command(pass_context=True)
    async def meme(self, ctx):
        embed = discord.Embed(title="", description="")

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))

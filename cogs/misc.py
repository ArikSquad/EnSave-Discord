import asyncio
import secrets

import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle

from db import config


class Misc(commands.Cog, description="Miscellaneous commands"):
    """
    Miscellaneous commands.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help=config.misc['sayCommandDescription'],
                      name=config.misc['sayCommandName'],
                      aliases=["tell", "echo", "speak"])
    async def say(self, ctx, *, text):
        msg = discord.Embed(title="Misc",
                            description=f'' + ctx.message.author.mention + ': ' + text,
                            color=discord.Color.green())
        async with ctx.typing():
            await asyncio.sleep(2)
        await ctx.send(embed=msg)

    @commands.command(help="Says hello to you", hidden=True)
    async def hello(self, ctx):
        msg = discord.Embed(title="Misc",
                            description=f"Hello {ctx.author.name}",
                            color=discord.Color.green())
        await ctx.send(embed=msg)

    @commands.command(
        aliases=["pfp", "av", "profilepicture", "profile"], name="Avatar"
    )
    async def avatar(self, ctx, *, member: discord.Member = None):
        if not member:
            member = ctx.message.author

        a = member.avatar_url
        ctx.send(a)

    @commands.command(name="Slap", description="Slap someone")
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def slap(self, ctx, member: discord.User = None):
        emb = discord.Embed(title="Misc",
                            description=f"{ctx.message.author.mention} slaps {member.mention} in the face!",
                            color=0x3498db)

        await ctx.send(embed=emb)

    @commands.command(help=config.misc['websiteCommandDescription'], name=config.misc['websiteCommandName'])
    async def website(self, ctx):

        embed = discord.Embed(title=f"Website", color=discord.Color.gold())

        await ctx.send(
            embed=embed,
            components=[
                Button(style=ButtonStyle.URL, label="Website", url="http://www.mikart.eu"),
                Button(style=ButtonStyle.URL, label="Docs", url="http://docs.mikart.eu"),
            ],
        )

    @commands.command(name="Password")
    async def password(self, ctx, nbytes: int = 18):
        """ Generates a random password string for you
        This returns a random URL-safe text string, containing nbytes random bytes.
        The text is Base64 encoded, so on average each byte results in approximately 1.3 characters.
        """

        embed1 = discord.Embed(title=f"Misc", description="I only accept any numbers between 3-1400",
                               color=discord.Color.dark_red())

        embed2 = discord.Embed(title=f"Misc", description=f"Sending you a private message with your "
                                                          f"random generated password **{ctx.author.name}**",
                               color=discord.Color.green())

        embed3 = discord.Embed(title=f"Misc", description=f"🎁 **Here is your "
                                                          f"password:**\n{secrets.token_urlsafe(nbytes)}",
                               color=discord.Color.green())

        if nbytes not in range(3, 1401):
            return await ctx.send(embed=embed1)
        if hasattr(ctx, "guild") and ctx.guild is not None:
            await ctx.send(embed=embed2)
        await ctx.author.send(embed=embed3)


def setup(bot):
    bot.add_cog(Misc(bot))

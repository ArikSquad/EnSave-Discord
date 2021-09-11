import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext
import random
import aiohttp

guild_ids = [770634445370687519]


class Slash(commands.Cog, description="Slash Commands"):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="meme", guild_ids=guild_ids, description="Memes!")
    async def _meme(self, ctx: SlashContext):
        numbercheck = random.randint(1, 5)
        if numbercheck == 2:
            embed = discord.Embed(title=f"Join minecraft server Play.MikArt.eu", description="")
        else:
            embed = discord.Embed(title="Memes", description="")
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
                res = await r.json()
                embed.set_image(url=res['data']['children'][random.randint(0, 25)]['data']['url'])
                await ctx.send(embed=embed)

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


def setup(bot):
    bot.add_cog(Slash(bot))

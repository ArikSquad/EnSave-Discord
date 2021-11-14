import discord
from discord.ext import commands

from db import config


class Music(commands.Cog, description=config.music['description']):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(help=config.music['airmaxCommandDescription'], name=config.music['airmaxCommandName'])
    async def airmax(self, ctx):
        msg = discord.Embed(title=config.music['name'],
                            description=config.music['playingMusic'] + config.music['airmaxCommandNameFull'],
                            color=discord.Color.green())
        await ctx.send(embed=msg)
        if ctx.author.voice.channel:
            if not ctx.guild.voice_client:  # error would be thrown if bot already connected, this stops the error
                player = await ctx.author.voice.channel.connect()
            else:
                player = ctx.guild.voice_client
            player.play(discord.FFmpegPCMAudio("music/airmaxviolin.mp3"))  # or "path/to/your.mp3"
        else:
            await ctx.send(config.music['musicFailed'])


def setup(bot: commands.Bot):
    bot.add_cog(Music(bot))


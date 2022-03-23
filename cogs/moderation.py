# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

import discord
from discord.ext import commands


class Moderation(commands.Cog, description="Moderation commands.."):
    COG_EMOJI = "📏"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='lock', aliases=['lockdown'], description="Locks the channel.", usage="lock")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        await ctx.message.delete()
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)

        embed = discord.Embed(title="Channel Locked", description="Channel has been locked.", color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(name='unlock', aliases=['unlockdown'], description="Unlocks the channel.", usage="unlock")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        await ctx.message.delete()
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)

        embed = discord.Embed(title="Channel Unlocked", description="Channel has been unlocked.", color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(name='clear', aliases=['purge'], description="Clears the channel.", usage="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)

        embed = discord.Embed(title="Messages Cleared", description=f"{amount} messages have been cleared.", color=0x00ff00)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))

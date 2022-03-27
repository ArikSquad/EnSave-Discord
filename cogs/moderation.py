# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import datetime

import discord
from discord.ext import commands


class Moderation(commands.Cog, description="Moderation commands.."):
    COG_EMOJI = "📏"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lock", help="Locks the channel.", aliases=['lockdown'])
    @commands.has_permissions(manage_channels=True, manage_messgaes=True)
    async def lock(self, ctx, channel: discord.TextChannel = None, reason: str = None):
        channel = ctx.channel or channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False, add_reactions=False)
        await ctx.send(f"Successfully locked {channel.mention}",
                       ephemeral=True)

        embed = discord.Embed(
            title="Channel locked",
            description=f"This channel was locked by {ctx.author.mention} 🔒",
            color=discord.Color.dark_red()
        )
        embed.add_field(name="Reason", value=reason.capitalize())
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)

    @commands.command(name='unlock', aliases=['unlockdown'], help="Unlocks the channel.")
    @commands.has_permissions(manage_channels=True, manage_messgaes=True)
    async def unlock(self, ctx):
        await ctx.message.delete()
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True, add_reactions=True)

        embed = discord.Embed(title="Channel Unlocked",
                              description="Channel has been unlocked.",
                              color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name='clear', aliases=['purge'], help="Clears the channel.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)

        embed = discord.Embed(title="Messages Cleared",
                              description=f"{amount} messages have been cleared.",
                              color=0x00ff00)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))

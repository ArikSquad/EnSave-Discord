# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import asyncio
import datetime

import discord
from discord import app_commands
from discord.ext import commands

from utils import db


class Moderation(commands.Cog, description="Moderating"):
    EMOJI = "📏"

    def __init__(self, bot):
        self.bot = bot

    # Command to lock a channel, so nobody else than moderators can send messages
    @app_commands.command(name="lock", description="Locks the channel, so people can't send messages.")
    @commands.has_permissions(manage_channels=True, manage_messages=True)
    async def lock(self, ctx: commands.Context, channel: discord.TextChannel = None,
                   reason: str = None, notify: bool = True):
        channel = ctx.channel or channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=False, add_reactions=False)
        vanish_name = "nobody"
        embed = discord.Embed(
            title="Channel locked",
            description=f"This channel was locked by {ctx.author.mention if notify else vanish_name} 🔒",
            color=discord.Color.dark_red()
        )
        embed.add_field(name="Reason", value=str(reason).capitalize() if not None else "No reason given.")
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)

    # Command to unlock a channel, so everybody can send messages again
    @app_commands.command(name='unlock', description="Unlocks the channel.")
    @commands.has_permissions(manage_channels=True, manage_messages=True)
    async def unlock(self, ctx: commands.Context, channel: discord.TextChannel = None):
        channel = ctx.channel or channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True, add_reactions=True)

        embed = discord.Embed(title="Channel Unlocked",
                              description="This channel has been unlocked.",
                              color=discord.Color.green())
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)

    # Command to delete messages in the channel
    @app_commands.command(name='clear', description="Clear an amount of messages from the channel.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)

        embed = discord.Embed(title="Messages Cleared",
                              description=f"{amount} messages have been cleared.",
                              color=0x00ff00)
        message = await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await message.delete()

    # Command to change the bot prefix for a guild
    @app_commands.command(name="change-prefix", description="Change the prefix of the guild.")
    @commands.has_permissions(administrator=True)
    async def change_prefix(self, ctx: commands.Context, prefix: str):
        embed = discord.Embed(title="Moderation",
                              description=f"Changed the prefix to: " + prefix,
                              color=discord.Color.gold())
        await ctx.send(embed=embed)

        db.set_guild_prefix(ctx.guild.id, prefix)

        print(f'Changed prefix in {ctx.guild} to {prefix}. Command was ran user {ctx.message.author}.')


async def setup(bot):
    await bot.add_cog(Moderation(bot))

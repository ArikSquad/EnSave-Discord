# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import datetime
import json

import discord
from discord.ext import commands


class Moderation(commands.Cog, description="Moderating"):
    COG_EMOJI = "📏"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lock", help="Locks the channel.", aliases=['lockdown'])
    @commands.has_permissions(manage_channels=True, manage_messages=True)
    async def lock(self, ctx, channel: discord.TextChannel = None, reason: str = None, notify: bool = True):
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

    @commands.command(name='unlock', aliases=['unlockdown'], help="Unlocks the channel.")
    @commands.has_permissions(manage_channels=True, manage_messages=True)
    async def unlock(self, ctx, channel: discord.TextChannel = None):
        channel = ctx.channel or channel
        await channel.set_permissions(ctx.guild.default_role, send_messages=True, add_reactions=True)

        embed = discord.Embed(title="Channel Unlocked",
                              description="This channel has been unlocked.",
                              color=discord.Color.green())
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)

    @commands.command(name='clear', aliases=['purge'], help="Clears the channel.")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)

        embed = discord.Embed(title="Messages Cleared",
                              description=f"{amount} messages have been cleared.",
                              color=0x00ff00)
        await ctx.send(embed=embed)

    @commands.command(name="prefix", help="Change the prefix of the guild.",
                      aliases=["changeprefix"])
    @commands.has_permissions(administrator=True)
    async def change_prefix(self, ctx, prefix):
        embed = discord.Embed(title="Moderation",
                              description=f"Changed the prefix to: " + prefix,
                              color=discord.Color.gold())
        await ctx.send(embed=embed)

        with open('db/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefixes[str(ctx.guild.id)] = prefix

        with open('db/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        print(f'Changed prefix in {ctx.guild} to {prefix}. Command was ran user {ctx.message.author}.')


async def setup(bot):
    await bot.add_cog(Moderation(bot))

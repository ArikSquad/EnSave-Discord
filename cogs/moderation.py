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


class Moderation(commands.Cog, description="Moderation commands.."):
    COG_EMOJI = "📏"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lock", help="Locks the channel.", aliases=['lockdown'])
    @commands.has_permissions(manage_channels=True, manage_messages=True)
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
    @commands.has_permissions(manage_channels=True, manage_messages=True)
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

    # This command was forked from
    # https://github.com/Carberra/updated-discord.py-tutorial/blob/085113e9bff69a699a25ed1cd91db5744b8755ea/lib/cogs/info.py#L37
    @commands.command(name="serverinfo", aliases=["guildinfo", "si", "gi"])
    @commands.has_permissions(administrator=True)
    async def server_info(self, ctx):
        embed = discord.Embed(title="Server information",
                              colour=ctx.guild.owner.colour,
                              timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url=ctx.guild.icon.url)

        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        fields = [("ID", ctx.guild.id, True),
                  ("Owner", ctx.guild.owner, True),
                  ("Created at", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), True),
                  ("Members", len(ctx.guild.members), True),
                  ("Users", len(list(filter(lambda m: not m.bot, ctx.guild.members))), True),
                  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), True),
                  ("Banned members", len(await ctx.guild.bans()), True),
                  ("Statuses", f"🟢 {statuses[0]} 🟠 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", True),
                  ("Text channels", len(ctx.guild.text_channels), True),
                  ("Voice channels", len(ctx.guild.voice_channels), True),
                  ("Categories", len(ctx.guild.categories), True),
                  ("Roles", len(ctx.guild.roles), True),
                  ("Invites", len(await ctx.guild.invites()), True),
                  ("\u200b", "\u200b", True)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

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

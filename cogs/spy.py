# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import discord
from discord import app_commands
from discord.ext import commands

from utils import db


class Spy(commands.Cog, description="Spying"):
    EMOJI = "🕵️"

    def __init__(self, bot):
        self.bot = bot

    # When a message is edited, send a message in the spy channel
    @commands.Cog.listener()
    async def on_message_edit(self, before, after) -> None:
        spy = db.get_guild_spy(before.guild.id)
        spy_channel = db.get_guild_spy_channel(before.guild.id)

        if spy and spy_channel:
            if before.author.bot:
                return
            if before.content == after.content:
                return
            embed = discord.Embed(
                title="Message edited",
                description=f"{before.author.mention} message was edited",
                color=discord.Color.blue(),
            )
            embed.add_field(name="Before", value=before.content, inline=False)
            embed.add_field(name="After", value=after.content, inline=False)
            embed.set_footer(text=f"Message ID: {before.id}")

            channel = self.bot.get_channel(spy_channel)
            await channel.send(embed=embed)

    # When a message is deleted, send a message in the spy channel
    @commands.Cog.listener()
    async def on_message_delete(self, message) -> None:
        spy = db.get_guild_spy(message.guild.id)
        spy_channel = db.get_guild_spy_channel(message.guild.id)

        if spy and spy_channel:
            if message.author.bot:
                return
            embed = discord.Embed(
                title="Message deleted",
                description=f"{message.author.mention} message was deleted.",
                color=discord.Color.red(),
            )
            embed.add_field(name="Message", value=message.content)
            embed.set_footer(text=f"Message ID: {message.id}")

            channel = self.bot.get_channel(spy_channel)
            await channel.send(embed=embed)

    # Toggle the spying on a server
    @app_commands.command(name="spy",
                          description="Toggle spying on the server.")
    @commands.has_permissions(manage_guild=True)
    async def spy(self, ctx: commands.Context, channel: discord.TextChannel, toggle: bool = None) -> None:
        if toggle:
            value = 1 if toggle is True else 0
            db.set_guild_spy(ctx.guild.id, value)
        else:
            db.set_guild_spy(ctx.guild.id, not db.get_guild_spy(ctx.guild.id))

        db.set_guild_spy_channel(ctx.guild.id, channel.id)

        toggled = "enabled" if toggle else "disabled"
        embed = discord.Embed(
            title="Spy",
            description=f"Spying is now {toggled} on the channel {channel.name}.",
            color=discord.Color.green(),
        )

        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Spy(bot))

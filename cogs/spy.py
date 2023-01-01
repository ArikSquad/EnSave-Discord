# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2021-2023 MikArt
# Released under the Apache License 2.0
#
# -----------------------------------------------------------
import discord
from discord import app_commands
from discord.ext import commands

from utils import db


class Spy(commands.Cog, description="Spying"):
    def __init__(self, bot):
        self.bot = bot

    # When a message is edited, send a message in the spy channel
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message) -> None:
        spy = db.get_guild_spy(before.guild.id)
        spy_channel = db.get_guild_spy_channel(before.guild.id)

        if spy and spy_channel:
            if before.author.bot:
                return
            if before.content == after.content:
                return

            embed = discord.Embed(
                title="Message edited",
                description=f"A message sent by {before.author.mention} was edited",
                color=discord.Color.blue(),
            )
            embed.add_field(name="Before", value=before.content, inline=False)
            embed.add_field(name="After", value=after.content, inline=False)
            embed.add_field(name="Channel", value=before.channel.mention, inline=False)
            embed.add_field(name="Time changed", value=after.edited_at, inline=False)
            embed.add_field(name="Message link", value=before.jump_url, inline=False)
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
                description=f"A message sent by {message.author.mention} was deleted",
                color=discord.Color.red(),
            )
            embed.add_field(name="Message", value=message.content)
            embed.add_field(name="Channel", value=message.channel.mention)
            embed.add_field(name="Time posted", value=message.created_at.strftime("%d/%m/%Y %H:%M:%S"))
            embed.set_footer(text=f"Message ID: {message.id}")

            channel = self.bot.get_channel(spy_channel)
            await channel.send(embed=embed)

    # Toggle the spying on a server
    @app_commands.command(name="spy",
                          description="Enable or disable message editing or deleting messages.")
    @app_commands.checks.has_permissions(manage_guild=True)
    @app_commands.guild_only()
    async def spy(self, interaction: discord.Interaction,
                  notify_channel: discord.TextChannel, toggle: bool) -> None:
        db.set_guild_spy(interaction.guild.id, 1 if toggle is True else 0)
        db.set_guild_spy_channel(interaction.guild.id, notify_channel.id)

        embed = discord.Embed(
            title="Spy",
            description=f"Spying is now {'enabled' if toggle else 'disabled'} "
                        f"{f'on the channel {notify_channel.name}.' if notify_channel else ''}",
            color=discord.Color.green(),
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Spy(bot))

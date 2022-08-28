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


class Moderation(commands.Cog, description="Moderating"):
    def __init__(self, bot):
        self.bot = bot

    # Command to lock a channel, so nobody else than moderators can send messages
    @app_commands.command(name="lock", description="Locks the channel, so people can't send messages.")
    @app_commands.checks.has_permissions(manage_channels=True, manage_messages=True)
    @app_commands.guild_only()
    async def lock(self, interaction: discord.Interaction, channel: discord.TextChannel = None,
                   reason: str = None, notify: bool = True):
        channel = interaction.channel if interaction.channel else channel
        await channel.set_permissions(interaction.guild.default_role, send_messages=False, add_reactions=False)
        vanish_name = f' by {interaction.user.name}' if notify else ' by nobody'
        embed = discord.Embed(
            title="Channel locked",
            description=f"This channel was locked{vanish_name} 🔒",
            color=discord.Color.from_rgb(48, 50, 54)
        )
        embed.add_field(name="Reason", value=str(reason).capitalize() if not None else "No reason given.")
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)
        await interaction.response.defer()

    # Command to unlock a channel, so everybody can send messages again
    @app_commands.command(name='unlock', description="Unlocks the channel.")
    @app_commands.checks.has_permissions(manage_channels=True, manage_messages=True)
    @app_commands.guild_only()
    async def unlock(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        channel = interaction.channel if interaction.channel else channel
        await channel.set_permissions(interaction.guild.default_role, send_messages=True, add_reactions=True)

        embed = discord.Embed(title="Channel Unlocked",
                              description="This channel has been unlocked.",
                              color=discord.Color.from_rgb(48, 50, 54))
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)
        await interaction.response.defer()

    # Command to delete messages in the channel
    @app_commands.command(name='clear', description="Clear an amount of messages from the channel.")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.guild_only()
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.message.delete()
        await interaction.channel.purge(limit=amount)

        embed = discord.Embed(title="Messages Cleared",
                              description=f"{amount} messages have been cleared.",
                              color=discord.Color.from_rgb(48, 50, 54))
        message = await interaction.response.send_message(embed=embed)
        await asyncio.sleep(5)
        await message.delete()


async def setup(bot):
    await bot.add_cog(Moderation(bot))

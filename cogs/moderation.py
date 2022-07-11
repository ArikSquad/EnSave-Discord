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
    @app_commands.checks.has_permissions(manage_channels=True, manage_messages=True)
    async def lock(self, interaction: discord.Interaction, channel: discord.TextChannel = None,
                   reason: str = None, notify: bool = True):
        channel = interaction.channel or channel
        await channel.set_permissions(interaction.guild.default_role, send_messages=False, add_reactions=False)
        vanish_name = "nobody"
        embed = discord.Embed(
            title="Channel locked",
            description=f"This channel was locked by {interaction.user.mention if notify else vanish_name} 🔒",
            color=discord.Color.from_rgb(48, 50, 54)
        )
        embed.add_field(name="Reason", value=str(reason).capitalize() if not None else "No reason given.")
        embed.timestamp = datetime.datetime.utcnow()
        await channel.send(embed=embed)
        await interaction.response.defer()

    # Command to unlock a channel, so everybody can send messages again
    @app_commands.command(name='unlock', description="Unlocks the channel.")
    @app_commands.checks.has_permissions(manage_channels=True, manage_messages=True)
    async def unlock(self, interaction: discord.Interaction, channel: discord.TextChannel = None):
        channel = interaction.channel or channel
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
    async def clear(self, interaction: discord.Interaction, amount: int):
        await interaction.message.delete()
        await interaction.channel.purge(limit=amount)

        embed = discord.Embed(title="Messages Cleared",
                              description=f"{amount} messages have been cleared.",
                              color=discord.Color.from_rgb(48, 50, 54))
        message = await interaction.response.send_message(embed=embed)
        await asyncio.sleep(5)
        await message.delete()

    # Command to change the bot prefix for a guild
    @app_commands.command(name="change-prefix", description="Change the prefix of the guild.")
    @app_commands.checks.has_permissions(administrator=True)
    async def change_prefix(self, interaction: discord.Interaction, prefix: str):
        if len(prefix) > 5:
            await interaction.response.send_message("The prefix can't be longer than 5 characters.", ephemeral=True)
            return
        embed = discord.Embed(title="Moderation",
                              description=f"Changed the prefix to: " + prefix,
                              color=discord.Color.gold())
        await interaction.response.send_message(embed=embed)

        db.set_guild_prefix(interaction.guild.id, prefix)

    @app_commands.command(name="get-prefix", description="Get the prefix of the guild.")
    async def get_prefix(self, interaction: discord.Interaction):
        prefix = db.get_guild_prefix(interaction.guild.id)
        embed = discord.Embed(title="Moderation",
                              description=f"The prefix of this guild is: " + prefix,
                              color=discord.Color.from_rgb(48, 50, 54))
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Moderation(bot))

# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
# -----------------------------------------------------------
import datetime
import traceback

import aiohttp
import discord
from discord.ext import commands

from utils import utility


def error_formatter(error, maxlength):
    v = ''

    for line in traceback.format_tb(error.__traceback__):
        if len(v) + len(line) > maxlength:
            return v
        v = f'{v}\n{line}'
    if len(v) > 0:
        return v


# This cog will send the message to the owner, when an error has ocurred.
class Errorhandler(commands.Cog, description="Errorhandler"):
    def __init__(self, bot):
        self.bot = bot
        bot.tree.on_error = self.on_app_command_error

    async def traceback(self, interaction: discord.Interaction, embed: discord.Embed):
        owner: list = utility.get_owner()
        for _owner_id in owner:
            _owner = self.bot.get_user(_owner_id)
            if _owner is None:
                continue

            channel = _owner.dm_channel if _owner.dm_channel else await _owner.create_dm()

            if not channel:
                return

            perms = channel.permissions_for(interaction.guild.me if interaction.guild else None)
            if not perms.view_channel or not perms.send_messages or not perms.embed_links:
                return

            await channel.send(embed=embed)

    _error_messages = {
        commands.NoPrivateMessage: 'This command cannot be used in private messages',
        commands.BotMissingPermissions: '{err}',
        commands.DisabledCommand: 'This command is disabled and cannot be used',
        commands.CheckFailure: '{err}',
        commands.CommandOnCooldown: '{err}',
        commands.errors.CommandOnCooldown: '{err}',
        commands.MissingRequiredArgument: 'You are missing a required argument! ',
        commands.BadArgument: 'Invalid argument given!',
        commands.CommandNotFound: None,
        commands.UserInputError: 'Invalid command usage!',
        aiohttp.ClientConnectorError: 'The EnSave music servers are currently offline, '
                                      'please retry later as they restart.'
    }

    async def on_app_command_error(self, interaction: discord.Interaction, error):
        classname = error.__class__
        if classname in self._error_messages.keys():
            msg = self._error_messages.get(classname, None)
            if isinstance(msg, str):
                if interaction.response.is_done():
                    interaction.followup.send(msg.format(interaction=interaction, err=error))
                else:
                    await interaction.response.send_message(msg.format(interaction=interaction, err=error))
        else:

            if isinstance(error, (commands.CommandError, commands.CheckFailure)) \
                    and not isinstance(error, commands.CommandInvokeError):
                error_embed = discord.Embed(
                    title=f'Something went wrong',
                    description=f'{error}',
                    color=discord.Color.red()
                )
                error_embed.add_field(name='Command Information',
                                      value=f'Command: {interaction.command}\n'
                                            f'Description: {interaction.command.description}\n'
                                            f'Cog: {interaction.command.cog.qualified_name}\n')
                if interaction.response.is_done():
                    return await interaction.followup.send(embed=error_embed)
                else:
                    return await interaction.response.send_message(embed=error_embed)

            execute_error = discord.Embed(
                color=discord.Colour(0xff0000),
                title='An error occured while trying to execute that command, '
                      'Please contact ArikSquad#6222',
                timestamp=datetime.datetime.utcnow()
            )
            if interaction.response.is_done():
                await interaction.followup.send(embed=execute_error)
            else:
                await interaction.response.send_message(embed=execute_error)

            print(error.original)

            embed = discord.Embed(
                color=discord.Colour(0xff0000),
                title='Command execution failed',
                timestamp=datetime.datetime.utcnow()
            )

            embed.add_field(name='Command', value=interaction.command.name)
            embed.add_field(name='Channel',
                            value='Private Message' if isinstance(interaction.channel,
                                                                  discord.DMChannel)
                            else f'#{interaction.channel.name}'
                                 f' (`{interaction.channel.id}`)')
            embed.add_field(name='Sender', value=f'{interaction.user} (`{interaction.user.id}`)')
            embed.add_field(name='Exception', value=str(error))
            formatted_traceback = error_formatter(error.original, 4094)
            embed.description = f'```py\n{formatted_traceback}```'

            await self.traceback(interaction, embed)


async def setup(bot):
    await bot.add_cog(Errorhandler(bot))

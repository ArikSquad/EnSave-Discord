# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# This file is not protected by any license
#
# -----------------------------------------------------------
import datetime
import traceback

import aiohttp
import discord
from discord.ext import commands


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
    EMOJI = "❌"

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def traceback(ctx: commands.Context, embed: discord.Embed):
        app_info = await ctx.bot.application_info()

        channel = app_info.owner.dm_channel if app_info.owner.dm_channel else await app_info.owner.create_dm()

        if not channel:
            return

        perms = channel.permissions_for(ctx.guild.me if ctx.guild else None)
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
        commands.MissingRequiredArgument: 'You are missing a required argument! '
                                          '(See `{ctx.prefix}help {ctx.command.qualified_name}` '
                                          'for info on how to use this command).',
        commands.BadArgument: 'Invalid argument given! (See `{ctx.prefix}help {ctx.command.qualified_name}` '
                              'for info on how to use this command).',
        commands.CommandNotFound: None,
        commands.UserInputError: 'Invalid command usage! (See `{ctx.prefix}help {ctx.command.qualified_name}` ',
        aiohttp.ContentTypeError: 'Something went wrong. This usually happens when you use music commands.',
    }

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        classname = error.__class__
        if classname in self._error_messages.keys():
            msg = self._error_messages.get(classname, None)
            if isinstance(msg, str):
                await ctx.send(msg.format(ctx=ctx, err=error))
        else:

            if isinstance(error, (commands.CommandError, commands.CheckFailure)) \
                    and not isinstance(error, commands.CommandInvokeError):
                error_embed = discord.Embed(
                    title=f'Something went wrong',
                    description=f'{error}',
                    color=discord.Color.red()
                )
                error_embed.add_field(name='Command Information', value=f'Command: {ctx.command}\n'
                                                                        f'Description: {ctx.command.help}\n'
                                                                        f'Cog: {ctx.command.cog.qualified_name}\n')
                error_embed.set_footer(text=f'You can also try .help {ctx.command.qualified_name}')
                return await ctx.send(embed=error_embed)

            execute_error = discord.Embed(
                color=discord.Colour(0xff0000),
                title='An error occured while trying to execute that command, '
                      'Please contact ArikSquad#6222',
                timestamp=datetime.datetime.utcnow()
            )

            await ctx.send(embed=execute_error)

            print(error.original)

            embed = discord.Embed(
                color=discord.Colour(0xff0000),
                title='Command execution failed',
                timestamp=datetime.datetime.utcnow()
            )

            embed.add_field(name='Command', value=ctx.command)
            embed.add_field(name='Original message',
                            value=ctx.message.content[:1021] + (ctx.message.content[1021:] and '...'))
            embed.add_field(name='Channel',
                            value='Private Message' if isinstance(ctx.channel,
                                                                  discord.DMChannel) else f'#{ctx.channel.name}'
                                                                                          f' (`{ctx.channel.id}`)')
            embed.add_field(name='Sender', value=f'{ctx.author} (`{ctx.author.id}`)')
            embed.add_field(name='Exception', value=str(error))
            formatted_traceback = error_formatter(error.original, 4094)
            embed.description = f'```py\nCog {ctx.cog.qualified_name}\n{formatted_traceback}```'

            await self.traceback(ctx, embed)


async def setup(bot):
    await bot.add_cog(Errorhandler(bot))

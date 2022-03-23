# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

from discord.ext import commands

from utils import HelpCommand


class Help(commands.Cog, description="The help command."):
    """Shows help info for commands and cogs"""
    COG_EMOJI = "❔"

    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = HelpCommand.MyHelpCommand()
        bot.help_command.cog = self


async def setup(bot):
    await bot.add_cog(Help(bot))

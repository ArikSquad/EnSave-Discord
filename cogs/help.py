# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

from discord.ext import commands

from utils import helpCommand


class Help(commands.Cog, description="Help"):
    EMOJI = "📖"

    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command = helpCommand.HelpCommand()
        self.bot.help_command.cog = self


async def setup(bot):
    await bot.add_cog(Help(bot))

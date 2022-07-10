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

from utils import helpCommand, utility


class Help(commands.Cog, description="Helping new users"):
    EMOJI = "📖"

    def __init__(self, bot):
        self.bot = bot
        # Create the help command
        self.bot.help_command = helpCommand.HelpCommand(description="Stop it. Get some help.")
        self.bot.help_command.cog = self

    @app_commands.command(name="help", description="Stop it. Get some help.")
    async def _help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="EnSave", description=self.bot.description,
                              color=discord.Color.from_rgb(48, 50, 54))
        embed.add_field(name="Support", value="We have a [discord support server](https://discord.gg/WKTcnb86b7)")

        categories = []
        for cog in self.bot.cogs:
            cog: commands.Cog = self.bot.get_cog(cog)
            categories.append(
                f"{getattr(cog, 'EMOJI', None)} - ({cog.qualified_name})[https://ensave.mikart.eu/commands]")
        embed.add_field(name="Categories", value="\n".join(categories))
        embed.add_field(name="Commands", value=f"For more information about commands you can use "
                                               f"`{utility.get_prefix_id(interaction.guild.id)}help`")

        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Help(bot))

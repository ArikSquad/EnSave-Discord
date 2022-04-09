# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

import discord
from discord.ext import commands


class HelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        channel = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page)
            await channel.send(embed=embed)

    async def send_command_help(self, command):
        emoji = getattr(command.cog, "EMOJI", None)
        embed = discord.Embed(
            title=f'{emoji} {self.get_command_signature(command)}'
        )
        embed.add_field(name="Description", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_cog_help(self, cog):
        emoji = getattr(cog, "EMOJI", None)
        embed = discord.Embed(title=f'{emoji} {cog.qualified_name}')
        embed.add_field(name="Description", value=cog.description)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=f'{error}\nRemember that cogs are case sensitive.',
                              color=discord.Color.red())

        channel = self.get_destination()
        await channel.send(embed=embed)

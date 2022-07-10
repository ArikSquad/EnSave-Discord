# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

from typing import List, Optional, Set

import discord
from discord.ext import commands


class HelpDropdown(discord.ui.Select):
    def __init__(self, help_command: "HelpCommand", options: List[discord.SelectOption]):
        super().__init__(placeholder="Choose a category...", min_values=1, max_values=1, options=options)
        self._help_command = help_command

    async def callback(self, interaction: discord.Interaction):
        embed = (
            await self._help_command.cog_help_embed(self._help_command.context.bot.get_cog(self.values[0]))
            if self.values[0] != self.options[0].value
            else await self._help_command.bot_help_embed(self._help_command.get_bot_mapping())
        )
        await interaction.response.edit_message(embed=embed)


class HelpView(discord.ui.View):
    def __init__(self, help_command: "HelpCommand", options: List[discord.SelectOption], *,
                 timeout: Optional[float] = 120.0):
        super().__init__(timeout=timeout)
        self.add_item(HelpDropdown(help_command, options))
        self._help_command = help_command
        self.response = None

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True
        await self.response.edit(view=self)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return self._help_command.context.author == interaction.user


class HelpCommand(commands.MinimalHelpCommand):

    # noinspection PyMethodMayBeStatic
    def get_command_brief(self, command: commands.Command) -> str:
        return command.short_doc or "This command has no description."

    def get_command_signature(self, command):
        return f"{self.context.clean_prefix}{command.qualified_name} {command.signature}"

    async def _cog_select_options(self) -> List[discord.SelectOption]:
        options: List[discord.SelectOption] = [discord.SelectOption(
            label="Home",
            emoji="🏠",
            description="Go back to the main menu.",
        )]

        for cog, command_set in self.get_bot_mapping().items():
            filtered = await self.filter_commands(command_set, sort=True)
            if not filtered:
                continue
            emoji = getattr(cog, "EMOJI", None)
            options.append(discord.SelectOption(
                label=cog.qualified_name if cog else "No Category",
                emoji=emoji,
                description=cog.description[:100] if cog and cog.description else None
            ))

        return options

    async def _help_embed(
            self, title: str, description: Optional[str] = None, mapping: Optional[dict] = None,
            command_set: Optional[Set[commands.Command]] = None, set_author: bool = False
    ) -> discord.Embed:
        embed = discord.Embed(title=title, color=discord.Color.from_rgb(48, 50, 54))
        if description:
            embed.description = description
        if set_author:
            avatar = self.context.bot.user.avatar or self.context.bot.user.default_avatar
            embed.set_author(name=self.context.bot.user.name, icon_url=avatar.url)
        if command_set:
            # show help about all commands in the set
            filtered = await self.filter_commands(command_set, sort=True)
            for command in filtered:
                embed.add_field(
                    name=self.get_command_signature(command),
                    value=command.short_doc or "...",
                    inline=False
                )
        elif mapping:
            # add a short description of commands in each cog
            for cog, command_set in mapping.items():
                filtered = await self.filter_commands(command_set, sort=True)
                if not filtered:
                    continue
                name = cog.qualified_name if cog else "No category"
                emoji = getattr(cog, "EMOJI", None)
                cog_label = f"{emoji} {name}" if emoji else name
                # \u2002 is an en-space
                cmd_list = "\u2002".join(
                    f"`{self.context.clean_prefix}{cmd.name}`" for cmd in filtered
                )
                value = (
                    f"{cog.description}\n{cmd_list}"
                    if cog and cog.description
                    else cmd_list
                )
                embed.add_field(name=cog_label, value=value)
        return embed

    async def bot_help_embed(self, mapping: dict) -> discord.Embed:
        return await self._help_embed(
            title="Bot Commands",
            description=self.context.bot.description,
            mapping=mapping,
            set_author=True,
        )

    async def send_bot_help(self, mapping: dict):
        embed = await self.bot_help_embed(mapping)
        options = await self._cog_select_options()
        view = HelpView(self, options)
        view.response = await self.get_destination().send(embed=embed, view=view)

    async def send_command_help(self, command: commands.Command) -> None:
        emoji = getattr(command.cog, "EMOJI", None)
        emoji_string = emoji if emoji is not None else ""
        embed = discord.Embed(
            title=f'{emoji_string} {self.get_command_signature(command)}',
            color=discord.Color.from_rgb(48, 50, 54)
        )
        embed.add_field(name="Description", value=command.help)
        alias = command.aliases
        brief = command.brief
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
        if brief:
            embed.add_field(name="Small Explanation", value=brief)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_group_help(self, group: commands.Group) -> None:
        emoji = getattr(group.cog, "EMOJI", None)
        emoji_string = emoji if emoji is not None else ""
        embed = discord.Embed(
            title=f'{emoji_string} {self.get_command_signature(group)}',
            color=discord.Color.from_rgb(48, 50, 54)
        )
        embed.add_field(name="Description", value=group.help)
        # Tell all the subcommand names
        subcommands = group.commands
        if subcommands:
            subcommand_names = [f"`{c.name}`" for c in subcommands]
            embed.add_field(name="Subcommands", value=", ".join(subcommand_names), inline=False)
        alias = group.aliases
        brief = group.brief
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
        if brief:
            embed.add_field(name="Small Explanation", value=brief)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def cog_help_embed(self, cog: Optional[commands.Cog]) -> discord.Embed:
        if cog is None:
            return await self._help_embed(
                title=f"No category",
                command_set=self.get_bot_mapping()[None]
            )
        emoji = getattr(cog, "EMOJI", None)
        return await self._help_embed(
            title=f"{emoji} {cog.qualified_name}" if emoji else cog.qualified_name,
            description=cog.description,
            command_set=cog.get_commands()
        )

    async def send_cog_help(self, cog: commands.Cog):
        embed = await self.cog_help_embed(cog)
        await self.get_destination().send(embed=embed)

    async def send_error_message(self, error) -> None:
        embed = discord.Embed(title="Error", description=f'{error}\nRemember that cogs are case sensitive.',
                              color=discord.Color.from_rgb(48, 50, 54))

        channel = self.get_destination()
        await channel.send(embed=embed)

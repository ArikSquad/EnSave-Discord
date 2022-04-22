# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
from itertools import chain, starmap

import discord
from discord import ui
from discord.ext import commands, menus


# noinspection PyUnusedLocal
class MenuPages(ui.View, menus.MenuPages):
    def __init__(self, source, *, delete_message_after=True):
        super().__init__(timeout=60)
        self._source = source
        self.current_page = 0
        self.ctx = None
        self.message = None
        self.delete_message_after = delete_message_after

    async def start(self, ctx, *, channel=None, wait=False):
        await self._source._prepare_once()
        self.ctx = ctx
        self.message = await self.send_initial_message(ctx, ctx.channel)

    async def _get_kwargs_from_page(self, page):
        value = await super()._get_kwargs_from_page(page)
        if 'view' not in value:
            value.update({'view': self})
        return value

    async def interaction_check(self, interaction):
        return interaction.user == self.ctx.author

    @ui.button(emoji='⏪', style=discord.ButtonStyle.blurple)
    async def first_page(self, interaction: discord.Interaction, button):
        await self.show_page(0)
        await interaction.response.defer()

    @ui.button(emoji='⬅', style=discord.ButtonStyle.blurple)
    async def before_page(self, interaction: discord.Interaction, button):
        await self.show_checked_page(self.current_page - 1)
        await interaction.response.defer()

    @ui.button(emoji='⏹', style=discord.ButtonStyle.blurple)
    async def stop_page(self, interaction: discord.Interaction, button):
        self.stop()
        if self.delete_message_after:
            await self.message.delete(delay=0)

    @ui.button(emoji='➡', style=discord.ButtonStyle.blurple)
    async def next_page(self, interaction: discord.Interaction, button):
        await self.show_checked_page(self.current_page + 1)
        await interaction.response.defer()

    @ui.button(emoji='⏩', style=discord.ButtonStyle.blurple)
    async def last_page(self, interaction: discord.Interaction, button):
        await self.show_page(self._source.get_max_pages() - 1)
        await interaction.response.defer()


class PageSource(menus.ListPageSource):
    def __init__(self, data, helpcommand):
        super().__init__(data, per_page=6)
        self.helpcommand = helpcommand

    def format_command_help(self, no, command):
        signature = self.helpcommand.get_command_signature(command)
        docs = self.helpcommand.get_command_brief(command)
        return f"{no} {signature}\n{docs}"

    async def format_page(self, menu, entries):
        page = menu.current_page
        max_page = self.get_max_pages()
        starting_number = page * self.per_page + 1
        iterator = starmap(self.format_command_help, enumerate(entries, start=starting_number))
        page_content = "\n".join(iterator)
        embed = discord.Embed(
            title=f"Help Command [{page + 1}/{max_page}]",
            description=f'{page_content}',
            color=0xffcccb
        )
        author = menu.ctx.author
        embed.set_footer(text=f"Requested by {author}", icon_url=author.avatar.url)
        return embed


class HelpCommand(commands.MinimalHelpCommand):
    # noinspection PyMethodMayBeStatic
    def get_command_brief(self, command):
        return command.short_doc or "This command has no description."

    async def send_bot_help(self, mapping):
        commands_list = list(chain.from_iterable(mapping.values()))
        all_commands = await self.filter_commands(commands_list)
        formatter = PageSource(all_commands, self)
        menu = MenuPages(formatter, delete_message_after=True)
        await menu.start(self.context)

    async def send_command_help(self, command):
        emoji = getattr(command.cog, "EMOJI", None)
        emoji_string = emoji if emoji is not None else ""
        embed = discord.Embed(
            title=f'{emoji_string} {self.get_command_signature(command)}',
            color=discord.Color.blue()
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

    async def send_group_help(self, group) -> None:
        emoji = getattr(group.cog, "EMOJI", None)
        emoji_string = emoji if emoji is not None else ""
        embed = discord.Embed(
            title=f'{emoji_string} {self.get_command_signature(group)}',
            color=discord.Color.blue()
        )
        embed.add_field(name="Description", value=group.help)
        embed.add_field(name="Subcommands", value=group.commands)
        alias = group.aliases
        brief = group.brief
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
        if brief:
            embed.add_field(name="Small Explanation", value=brief)

    async def send_cog_help(self, cog):
        emoji = getattr(cog, "EMOJI", None)
        emoji_string = emoji if emoji is not None else ""
        embed = discord.Embed(title=f'{emoji_string} {cog.qualified_name}',
                              color=discord.Color.blue())
        embed.add_field(name="Description", value=cog.description)

        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=f'{error}\nRemember that cogs are case sensitive.',
                              color=discord.Color.red())

        channel = self.get_destination()
        await channel.send(embed=embed)

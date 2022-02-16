# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import random

import aiohttp
import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from utils import getter

guild_ids = getter.get_guild_ids()


class Misc(commands.Cog, description="Misc Commands"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="dog", guild_ids=guild_ids, description="Posts a fun dog picture in the chat!")
    async def dog(self, interaction: Interaction):
        choices = [1, 2, 3]
        title_text = "Dog"

        if random.choice(choices) == 1:
            title_text = "Aww cute!"
        elif random.choice(choices) == 2 & getter.get_premium(interaction.user.id):
            title_text = "Get bot premium for more cool commands!"

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://random.dog/woof.json') as r:
                data = await r.json()
                embed = nextcord.Embed(
                    title=title_text,
                    color=interaction.user.color
                )
                embed.set_image(url=data['url'])
                await interaction.send(embed=embed)

    @nextcord.slash_command(name="bot-invite", guild_ids=guild_ids, description='Get the invite link of the bot.')
    async def bot_invite(self, interaction: Interaction):
        embed = nextcord.Embed(
            title='Info',
            description=f'Invite me by clicking '
                        f'[here](https://discord.com/api/oauth2/userize?'
                        f'client_id=812808865728954399&permissions=8&redirect_uri='
                        f'http%3A%2F%2Fdiscord.mikart.eu%2F&scope=bot%20applications.commands).',
            color=0xD75BF4
        )
        await interaction.send(embed=embed)

    @commands.command(name='old_dated_command',
                      aliases=[
                          'dice', 'slot', 'cookie',
                          'coinflip', 'dog', 'invite'
                      ],
                      help='Remove commands that are unsupported from the list. (Slash commands)', hidden=True)
    async def old_dated(self, ctx):
        embed = nextcord.Embed(title=f"Slash Commands.",
                               description=f'The command you tried to run is no longer '
                                           f'supported without slash command.',
                               color=ctx.author.color)
        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))

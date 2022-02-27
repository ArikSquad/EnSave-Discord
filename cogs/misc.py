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
import requests
from better_profanity import profanity
from nextcord import Interaction
from nextcord.ext import commands

from utils import db

guild_ids = db.get_guild_ids()


class Misc(commands.Cog, description="Misc Commands"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="dog", guild_ids=guild_ids, description="Posts a fun dog picture in the chat!")
    async def dog(self, interaction: Interaction):
        choice = random.randint(1, 2)
        title_text = "Dog"

        if choice == 1:
            title_text = "Aww cute!"
        elif choice == 2:
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
                        f'[here](https://discord.com/api/oauth2/authorize?client_id='
                        f'812808865728954399&permissions=8&scope=bot%20applications.commands).',
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

    @nextcord.slash_command(name="define", guild_ids=guild_ids, description="Define a word!")
    async def define(self, interaction: Interaction, word: str):
        if profanity.contains_profanity(word):
            embed = nextcord.Embed(
                title="Error",
                description=f"{interaction.user.mention} The word you tried to check is inappropriate.!",
                color=interaction.user.color
            )
            return await interaction.send(embed=embed)
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en_Us/{word}")
        if response.status_code == 200:
            data = response.json()
            meanings = data[0]["meanings"][0]["definitions"][0]
            embed = nextcord.Embed(description=f"You asked for the definition of **{word}**!",
                                   color=interaction.user.color)
            embed.add_field(name="Definition", value=meanings["definition"], inline=False)
            embed.add_field(name="Example", value=meanings["example"], inline=False)
            await interaction.send(embed=embed)
        else:
            embed = nextcord.Embed(description="Something went wrong. Please try again later.",
                                   color=interaction.user.color)
            await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(Misc(bot))

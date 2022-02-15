# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

import asyncio
import random

import nextcord
from nextcord import Interaction
from nextcord.ext import commands

from utils import getter

guild_ids = getter.get_guild_ids()


class Game(commands.Cog, description="Game Commands"):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(name="cookie", guild_ids=guild_ids, description="Cookie game!")
    async def _cookie(self, interaction: Interaction):
        await interaction.send(embed=nextcord.Embed(title="🍪 Cookie is coming..."))
        await asyncio.sleep(3)
        await interaction.send("No one got the cookie :(")
        await asyncio.sleep(2)
        await interaction.send("Just kidding, you got the cookie! :)")

    @nextcord.slash_command(name="slot", guild_ids=guild_ids, description="Roll the slot machine!")
    async def _slot(self, interaction: Interaction):
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{interaction.user.name}**,"

        embed1 = nextcord.Embed(title=f"Games", description=f"{slotmachine} All matching, you won! 🎉",
                                color=nextcord.Color.green())
        embed2 = nextcord.Embed(title=f"Games", description=f"{slotmachine} 2 in a row, you won! 🎉",
                                color=nextcord.Color.purple())
        embed3 = nextcord.Embed(title=f"Games", description=f"{slotmachine} No match, you lost 😢",
                                color=nextcord.Color.red())

        if a == b == c:
            await interaction.send(embed=embed1)
        elif (a == b) or (a == c) or (b == c):
            await interaction.send(embed=embed2)
        else:
            await interaction.send(embed=embed3)

    @nextcord.slash_command(name="dice", guild_ids=guild_ids, description="Roll the dice!")
    async def _dice(self, interaction: Interaction):
        embed1 = nextcord.Embed(title=f"Games", description="Rolled a {}!".format(random.randint(1, 6)),
                                color=nextcord.Color.green())
        await interaction.send(embed=embed1)

    @nextcord.slash_command(name="coinflip", guild_ids=guild_ids, description="Flip a coin!")
    async def _coinflip(self, interaction: Interaction):
        determine_flip = [1, 0]
        if random.choice(determine_flip) == 1:
            embed = nextcord.Embed(title="Fun",
                                   description=f"{interaction.user.mention} Flipped coin, we got **Heads**!",
                                   color=interaction.user.color)
            await interaction.send(embed=embed)

        else:
            embed = nextcord.Embed(title="Fun",
                                   description=f"{interaction.user.mention} Flipped coin, we got **Tails**!",
                                   color=interaction.user.color)
            await interaction.send(embed=embed)


def setup(bot):
    bot.add_cog(Game(bot))

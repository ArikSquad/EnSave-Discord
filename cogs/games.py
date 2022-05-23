# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2021-2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

import datetime
import random

import discord
from discord import app_commands
from discord.ext import commands

from utils import database


class Games(commands.Cog, description="Fun game commands"):
    EMOJI = "🕹️"

    def __init__(self, bot) -> None:
        self.bot = bot

    # Slash command to roll the slot machine
    @app_commands.command(name="slot", description="Roll the slot machine!")
    async def slot(self, interaction: discord.Interaction):
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{interaction.user.name}**,"

        embed1 = discord.Embed(title=f"Games", description=f"{slotmachine} All matching, you won! 🎉",
                               color=discord.Color.green())
        embed2 = discord.Embed(title=f"Games", description=f"{slotmachine} 2 in a row, you won! 🎉",
                               color=discord.Color.purple())
        embed3 = discord.Embed(title=f"Games", description=f"{slotmachine} No match, you lost 😢",
                               color=discord.Color.red())

        if a == b == c:
            await interaction.response.send_message(embed=embed1)
        elif (a == b) or (a == c) or (b == c):
            await interaction.response.send_message(embed=embed2)
        else:
            await interaction.response.send_message(embed=embed3)

    # Slash command to roll the dice
    @app_commands.command(name="dice", description="Roll the dice!")
    async def dice(self, interaction: discord.Interaction):
        embed1 = discord.Embed(title=f"Games", description="Rolled a {}!".format(random.randint(1, 6)),
                               color=discord.Color.green())
        await interaction.response.send_message(embed=embed1)

    # Slash command to flip a coin
    @app_commands.command(name="coinflip", description="Flip a coin!")
    async def coinflip(self, interaction: discord.Interaction):
        determine_flip = [1, 0]
        if random.choice(determine_flip) == 1:
            embed = discord.Embed(title="Fun",
                                  description=f"{interaction.user.mention} Flipped coin, we got **Heads**!",
                                  color=interaction.user.color)
            await interaction.response.send_message(embed=embed)

        else:
            embed = discord.Embed(title="Fun",
                                  description=f"{interaction.user.mention} Flipped coin, we got **Tails**!",
                                  color=interaction.user.color)
            await interaction.response.send_message(embed=embed)

    # Slash command to slap someone
    @app_commands.command(name="slap", description="Slap someone!")
    async def slap(self, interaction: discord.Interaction, member: discord.Member):
        if member.id == 812808865728954399:
            dodge = discord.Embed(title=interaction.user.name,
                                  description=f"tried to slap me, but I dodged. 😑",
                                  color=interaction.user.color)
            await interaction.response.send_message(embed=dodge)
        elif interaction.user.id == member.id:
            embed = discord.Embed(title=interaction.user.name,
                                  description=f"tried to slap themselves, "
                                              f"but hit too hard and went to a coma for 10 seconds. 😑",
                                  color=interaction.user.color)
            try:
                await interaction.user.edit(timed_out_until=datetime.datetime.now() + datetime.timedelta(seconds=10))
            except commands.MissingPermissions:
                pass
            await interaction.response.send_message(embed=embed)
        elif database.get_premium(member.id):
            embed = discord.Embed(title=interaction.user.name,
                                  description=f"tried to slap {member.name}, but had no strength to hit "
                                              f"a premium user. 😑",
                                  color=interaction.user.color)
            await interaction.response.send_message(embed=embed)
        else:
            embed = discord.Embed(title=interaction.user.name,
                                  description=f"just slapped {member.mention} in the face!",
                                  color=interaction.user.color)
            await interaction.response.send_message(embed=embed)

    # Slash command to ask the 8ball a question
    @app_commands.command(name="8ball", description="Ask the magic 8ball a question!")
    async def eightball(self, interaction: discord.Interaction, *, question: str):
        responses = [
            "It is certain.",
            "It is decidedly so.",
            "Without a doubt.",
            "Yes - definitely.",
            "You may rely on it.",
            "As I see it, yes.",
            "Yes.",
            "Most likely.",
            "Outlook good.",
            "Signs point to yes.",
            "Reply hazy, try again.",
            "Better not tell you now.",
            "uwu",
            "no, not today!",
            "Very doubtful."]
        embed = discord.Embed(title="Magic 8ball",
                              description=f"{interaction.user.mention} asked: {question}\n"
                                          f"Magic 8ball: **{random.choice(responses)}**",
                              color=interaction.user.color)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Games(bot))

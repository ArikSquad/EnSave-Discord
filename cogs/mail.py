# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

import discord
from discord.ext import commands


class Mail(commands.Cog, description="Mailing commands."):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mail", aliases=["m"], description="Send a message to a user.")
    async def mail(self, ctx, user: discord.Member, *, message):
        await user.send(f"{ctx.author.mention} sent you a message: {message}")


async def setup(bot):
    await bot.add_cog(Mail(bot))

# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
from discord.ext import commands


class React(commands.Cog, description="React to messages"):
    EMOJI = "🎈"

    def __init__(self, bot):
        self.bot = bot

    # Reacts to a message inside MikArt when a new update comes.
    @commands.Cog.listener()
    async def on_message(self, message) -> None:
        if message.channel.id == 962313825464504360:
            if message.author.id == 962313982746714142:
                emoji = self.bot.get_emoji(854963304227930123)
                await message.add_reaction(emoji)


async def setup(bot):
    await bot.add_cog(React(bot))

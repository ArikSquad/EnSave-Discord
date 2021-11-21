from discord.ext import commands
from dislash import *


class Fun(commands.Cog, description="Technical and Fun Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # checks if the the message author is the bot
        if message.author.bot:
            # if it is then returns
            return
        # checks if the file is a video/music file
        for a in message.attachments:
            for e in ['3g2', '3gp', 'amv', 'asf', 'avi', 'drc', 'f4a', 'f4b', 'f4p', 'f4v', 'flv', 'gif', 'gifv',
                      'm2ts', 'm2v', 'm4p', 'm4v', 'mkv', 'mng', 'mov', 'mp2', 'mp4', 'mpe', 'mpeg', 'mpg', 'mpv',
                      'mts', 'mxf', 'nsv', 'ogg', 'ogv', 'qt', 'rm', 'rmvb', 'roq', 'svi', 'ts', 'vob', 'webm', 'wmv',
                      'yuv', 'mp3']:
                if a.filename[-len(e) - 1:] == f'.{e}':
                    # then it sends the funny pic
                    await message.channel.send(
                        'https://i2.wp.com/www.betameme.com/wp-content/'
                        'uploads/2018/02/thank-you-meme-puppy.jpg?fit=498%2C462&ssl=1')
                    return

    @message_command(name="Reverse")
    async def reverse(self, inter: ContextMenuInteraction):
        # Message commands always have only this ^ argument
        if inter.message.content:
            # Here we will send a reversed message to the chat
            await inter.respond(inter.message.content[::-1])
        else:
            # If the message contains nothing, then return.
            return


def setup(bot):
    bot.add_cog(Fun(bot))

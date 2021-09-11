import discord
from discord.ext import commands
import time


class Info(commands.Cog, description="Info commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Invite")
    async def invite(self, context):
        """
        Get the invite link of the bot to be able to invite it.
        """
        embed = discord.Embed(
            title="Info",
            description=f"Invite me by clicking"
                        f" [here](https://discord.com/api/oauth2/authorize?"
                        f"client_id=812808865728954399&permissions=8&redirect_uri="
                        f"http%3A%2F%2Fdiscord.mikart.eu%2F&scope=bot%20applications.commands).",
            color=0xD75BF4
        )
        try:
            await context.author.send(embed=embed)
            await context.send("I sent you a private message!")
        except discord.Forbidden:
            await context.send(embed=embed)

    @commands.command(pass_context=True, help="Shows the latency.", name="Ping")
    async def ping(self, ctx):
        wait = discord.Embed(title="Info",
                             description=f"Waiting the server to respond!",
                             color=discord.Color.red())

        before = time.monotonic()
        message = await ctx.send(embed=wait)
        ping = (time.monotonic() - before) * 1000

        waited = discord.Embed(title="Info",
                               description=f"Pong!  `{int(ping)}ms`",
                               color=discord.Color.green())
        await message.edit(embed=waited)
        print(f'Ping {int(ping)}ms')

    @commands.command(aliases=["supportserver", "feedbackserver", "discord"], name="Server")
    async def server(self, ctx):
        """ Get an invite to our support server! """

        embed = discord.Embed(title="Info",
                              description=f"**Here you go {ctx.author.name} 🍻**\nhttps://discord.gg/DpxkY3x",
                              color=discord.Color.green())

        embed2 = discord.Embed(title="Info",
                               description=f"**{ctx.author.name}** This is the feedback server!",
                               color=discord.Color.green())

        if isinstance(ctx.channel, discord.DMChannel) or ctx.guild.id != 86484642730885120:
            return await ctx.send(embed=embed)
        await ctx.send(embed=embed2)


def setup(bot):
    bot.add_cog(Info(bot))

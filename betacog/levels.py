import discord
import json
from discord.ext import commands


class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            with open('level.json', 'r') as f:
                users = json.load(f)
            await update_data(users, message.author, message.guild)
            await add_experience(users, message.author, 4)
            await level_up(users, message.author, message.channel)

            with open('level.json', 'w') as f:
                json.dump(users, f)
        await self.bot.process_commands(message)

    @commands.command(aliases=['rank', 'lvl'])
    async def level(self, ctx, member: discord.Member = None):
        if not member:
            user = ctx.message.author
            with open('level.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(ctx.guild.id)][str(user.id)]['level']
            exp = users[str(ctx.guild.id)][str(user.id)]['experience']

            embed = discord.Embed(title='Level {}'.format(lvl), description=f"{exp} XP ",
                                  color=discord.Color.green())
            embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
            await ctx.send(embed=embed)
        else:
            with open('level.json', 'r') as f:
                users = json.load(f)
            lvl = users[str(ctx.guild.id)][str(member.id)]['level']
            exp = users[str(ctx.guild.id)][str(member.id)]['experience']
            embed = discord.Embed(title='Level {}'.format(lvl), description=f"{exp} XP",
                                  color=discord.Color.green())
            embed.set_author(name=str(member), icon_url=member.avatar_url)
            await ctx.send(embed=embed)


async def update_data(users, user, server):
    if not str(server.id) in users:
        users[str(server.id)] = {}
        if not str(user.id) in users[str(server.id)]:
            users[str(server.id)][str(user.id)] = {}
            users[str(server.id)][str(user.id)]['experience'] = 0
            users[str(server.id)][str(user.id)]['level'] = 1
    elif not str(user.id) in users[str(server.id)]:
        users[str(server.id)][str(user.id)] = {}
        users[str(server.id)][str(user.id)]['experience'] = 0
        users[str(server.id)][str(user.id)]['level'] = 1


async def add_experience(users, user, exp):
    users[str(user.guild.id)][str(user.id)]['experience'] += exp


async def level_up(users, user, channel):
    experience = users[str(user.guild.id)][str(user.id)]['experience']
    lvl_start = users[str(user.guild.id)][str(user.id)]['level']
    lvl_end = int(experience ** (1 / 4))
    if str(user.guild.id) != '757383943116030074':
        if lvl_start < lvl_end:
            await channel.send('{} has leveled up to Level {}'.format(user.mention, lvl_end))
            users[str(user.guild.id)][str(user.id)]['level'] = lvl_end


def setup(bot):
    bot.add_cog(Levels(bot))

# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import json

import discord
from discord.ext import commands


class Welcome(commands.Cog, description="Welcome commands."):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            with open("db/config.json", "r") as f:
                data = json.load(f)
                welcome_channel = data[str(member.guild.id)]["welcome_channel"]
                toggle = data[str(member.guild.id)]["welcome_toggle"]
        except KeyError:
            with open("db/config.json", "r") as f:
                data = json.load(f)
            data[str(member.guild.id)]["welcome_channel"] = None
            with open("db/config.json", "w") as f:
                json.dump(data, f, indent=4)
        if toggle:
            try:
                get_channel = discord.utils.get(member.guild.channels, name="ensave-guard")
                channel_id = get_channel.id
                channel = self.bot.get_channel(channel_id)
            except AttributeError:
                channel = self.bot.get_channel(welcome_channel)
            if member.id == 537237654207725568:
                return
            else:
                await channel.send(f"Welcome {member.mention} to {member.guild.name}! "
                                   f"We have a Minecraft server play.mikart.eu!")

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        try:
            with open("db/config.json", "r") as f:
                data = json.load(f)
                welcome_channel = data[str(member.guild.id)]["welcome_channel"]
                toggle = data[str(member.guild.id)]["welcome_toggle"]
        except KeyError:
            with open("db/config.json", "r") as f:
                data = json.load(f)
            data[str(member.guild.id)]["welcome_channel"] = None
            with open("db/config.json", "w") as f:
                json.dump(data, f, indent=4)
        if toggle:
            try:
                get_channel = discord.utils.get(member.guild.channels, name="ensave-guard")
                channel_id = get_channel.id
                channel = self.bot.get_channel(channel_id)
            except AttributeError:
                channel = self.bot.get_channel(welcome_channel)
            if member.id == 537237654207725568:
                return
            else:
                await channel.send(f"{member.mention} has left {member.guild.name}! super sad :(")

    @commands.command(name="welcome-channel")
    @commands.has_permissions(manage_guild=True)
    async def welcome_channel(self, ctx, channel: discord.TextChannel = None):
        if channel is not None:
            try:
                with open("db/config.json", "r") as f:
                    data = json.load(f)
                data[str(ctx.guild.id)]["welcome_channel"] = channel.id
                await ctx.send(f"Welcome channel set to {channel.mention}.")
                with open("db/config.json", "w") as f:
                    json.dump(data, f, indent=4)
            except KeyError:
                with open("db/config.json", "r") as f:
                    data = json.load(f)
                data[str(ctx.guild.id)] = {}
                data[str(ctx.guild.id)]["welcome_channel"] = channel.id if channel else None
                with open("db/config.json", "w") as f:
                    json.dump(data, f, indent=4)
        else:
            try:
                with open("db/config.json", "r") as f:
                    data = json.load(f)
                channel_id = data[str(ctx.guild.id)]["welcome_channel"]
                channel = self.bot.get_channel(channel_id)
                await ctx.send(f"Welcome channel is currently set to {channel.mention}.")
            except KeyError:
                await ctx.send("Welcome channel is currently set to None.")

    @commands.command(name="welcome-toggle")
    @commands.has_permissions(manage_guild=True)
    async def welcome_toggle(self, ctx):
        try:
            with open("db/config.json", "r") as f:
                data = json.load(f)
            data[str(ctx.guild.id)]["welcome_toggle"] = not data[str(ctx.guild.id)]["welcome_toggle"]
            await ctx.send(f"Welcome toggle set to {data[str(ctx.guild.id)]['welcome_toggle']}.")
            with open("db/config.json", "w") as f:
                json.dump(data, f, indent=4)
        except KeyError:
            with open("db/config.json", "r") as f:
                data = json.load(f)
            data[str(ctx.guild.id)] = {}
            data[str(ctx.guild.id)]["welcome_toggle"] = True
            with open("db/config.json", "w") as f:
                json.dump(data, f, indent=4)


async def setup(bot):
    await bot.add_cog(Welcome(bot))

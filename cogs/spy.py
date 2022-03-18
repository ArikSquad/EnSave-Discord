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


class Spy(commands.Cog, description="Spying commands."):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        try:
            with open("db/config.json", "r") as f:
                data = json.load(f)
                spy = data[str(before.guild.id)]["spy_edit"]
                spy_channel = data[str(before.guild.id)]["spy_channel"]
            if spy:
                if before.author.bot:
                    return
                if before.content == after.content:
                    return
                embed = discord.Embed(
                    title="Message edited",
                    description=f"{before.author.mention} edited their message.",
                    color=discord.Color.blue(),
                )
                embed.add_field(name="Before", value=before.content)
                embed.add_field(name="After", value=after.content)
                embed.set_footer(text=f"Message ID: {before.id}")
                try:
                    get_channel = discord.utils.get(before.guild.channels, name="ensave-guard")
                    channel_id = get_channel.id
                    channel = self.bot.get_channel(channel_id)
                    await channel.send(embed=embed)
                except AttributeError:
                    channel = self.bot.get_channel(spy_channel)
                    await channel.send(embed=embed)
        except KeyError:
            with open("db/config.json", "r") as f:
                data = json.load(f)
            data[str(before.guild.id)] = {}
            data[str(before.guild.id)]["spy_edit"] = False
            data[str(before.guild.id)]["spy_delete"] = False
            data[str(before.guild.id)]["spy_channel"] = None
            with open("db/config.json", "w") as f:
                json.dump(data, f, indent=4)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            with open("db/config.json", "r") as f:
                data = json.load(f)
                spy = data[str(message.guild.id)]["spy_delete"]
                spy_channel = data[str(message.guild.id)]["spy_channel"]
            if spy:
                if message.author.bot:
                    return
                embed = discord.Embed(
                    title="Message deleted",
                    description=f"{message.author.mention} deleted their message.",
                    color=discord.Color.red(),
                )
                embed.add_field(name="Message", value=message.content)
                embed.set_footer(text=f"Message ID: {message.id}")
                try:
                    get_channel = discord.utils.get(message.guild.channels, name="ensave-guard")
                    channel_id = get_channel.id
                    channel = self.bot.get_channel(channel_id)
                    await channel.send(embed=embed)
                except AttributeError:
                    channel = self.bot.get_channel(spy_channel)
                    await channel.send(embed=embed)
        except KeyError:
            with open("db/config.json", "r") as f:
                data = json.load(f)
            data[str(message.guild.id)] = {}
            data[str(message.guild.id)]["spy_edit"] = False
            data[str(message.guild.id)]["spy_delete"] = False
            data[str(message.guild.id)]["spy_channel"] = None
            with open("db/config.json", "w") as f:
                json.dump(data, f, indent=4)

    # Toggle the spying on a server,
    # spy: bool (True/False)
    # mode: int 1/2 (1 = edit, 2 = delete)
    @commands.command(name="spy", aliases=["spy-edit", "spy-delete"], help="Toggle the spying on the server.")
    @commands.has_permissions(manage_guild=True)
    async def spy(self, ctx, spy: bool, mode: int = None):
        desc = "**Something went wrong...**"
        try:
            with open("db/config.json", "r") as f:
                data = json.load(f)
            if spy:
                if mode == 1:
                    desc = "editing"
                    data[str(ctx.guild.id)]["spy_edit"] = True
                elif mode == 2:
                    desc = "deleting"
                    data[str(ctx.guild.id)]["spy_delete"] = True
                elif mode is None:
                    desc = "editing and deleting"
                    data[str(ctx.guild.id)]["spy_delete"] = True
                    data[str(ctx.guild.id)]["spy_edit"] = True
                embed = discord.Embed(
                    title="Spy",
                    description="Spying is now disabled for " + desc + ".",
                    color=discord.Color.green(),
                )
                await ctx.send(embed=embed)
            else:
                if mode == 1:
                    desc = "editing"
                    data[str(ctx.guild.id)]["spy_edit"] = False
                elif mode == 2:
                    desc = "deleting"
                    data[str(ctx.guild.id)]["spy_delete"] = False
                elif mode is None:
                    desc = "deleting and editing"
                    data[str(ctx.guild.id)]["spy_delete"] = False
                    data[str(ctx.guild.id)]["spy_edit"] = False
                embed = discord.Embed(
                    title="Spy",
                    description="Spying is now disabled for " + desc + ".",
                    color=discord.Color.red(),
                )
                await ctx.send(embed=embed)
            with open("db/config.json", "w") as f:
                json.dump(data, f, indent=4)
        except KeyError:
            with open("db/config.json", "r") as f:
                data = json.load(f)
            data[str(ctx.guild.id)] = {}
            data[str(ctx.guild.id)]["spy_edit"] = False
            data[str(ctx.guild.id)]["spy_delete"] = False
            data[str(ctx.guild.id)]["spy_channel"] = None
            with open("db/config.json", "w") as f:
                json.dump(data, f, indent=4)

    @commands.command(name="spy-channel")
    @commands.has_permissions(manage_guild=True)
    async def spy_channel(self, ctx, channel: discord.TextChannel):
        try:
            with open("db/config.json", "r") as f:
                data = json.load(f)
            data[str(ctx.guild.id)]["spy_channel"] = channel.id
            await ctx.send(f"Spy channel set to {channel.mention}.")
            with open("db/config.json", "w") as f:
                json.dump(data, f, indent=4)
        except KeyError:
            with open("db/config.json", "r") as f:
                data = json.load(f)
            data[str(ctx.guild.id)] = {}
            data[str(ctx.guild.id)]["spy_edit"] = False
            data[str(ctx.guild.id)]["spy_delete"] = False
            data[str(ctx.guild.id)]["spy_channel"] = channel if channel else None
            with open("db/config.json", "w") as f:
                json.dump(data, f, indent=4)


async def setup(bot):
    await bot.add_cog(Spy(bot))

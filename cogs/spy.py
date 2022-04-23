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


class Spy(commands.Cog, description="Spying"):
    EMOJI = "🕵️"

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        with open("db/guilds.json", "r") as f:
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
                description=f"{before.author.mention} message was edited",
                color=discord.Color.blue(),
            )
            embed.add_field(name="Before", value=before.content, inline=False)
            embed.add_field(name="After", value=after.content, inline=False)
            embed.set_footer(text=f"Message ID: {before.id}")
            try:
                channel = self.bot.get_channel(spy_channel)
                await channel.send(embed=embed)
            except AttributeError:
                get_channel = discord.utils.get(before.guild.channels, name="ensave-guard")
                channel_id = get_channel.id
                channel = self.bot.get_channel(channel_id)
                await channel.send(embed=embed)
            finally:
                pass

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        with open("db/guilds.json", "r") as f:
            data = json.load(f)
            spy = data[str(message.guild.id)]["spy_delete"]
            spy_channel = data[str(message.guild.id)]["spy_channel"]
        if spy:
            if message.author.bot:
                return
            embed = discord.Embed(
                title="Message deleted",
                description=f"{message.author.mention} message was deleted.",
                color=discord.Color.red(),
            )
            embed.add_field(name="Message", value=message.content)
            embed.set_footer(text=f"Message ID: {message.id}")
            try:
                channel = self.bot.get_channel(spy_channel)
                await channel.send(embed=embed)
            except AttributeError:
                get_channel = discord.utils.get(message.guild.channels, name="ensave-guard")
                channel_id = get_channel.id
                channel = self.bot.get_channel(channel_id)
                await channel.send(embed=embed)
            finally:
                pass

    # Toggle the spying on a server,
    # spy: bool (True/False)
    # mode: int 1/2 (1 = edit, 2 = delete)
    @commands.command(name="spy", aliases=["spy-edit", "spy-delete"], help="Toggle the spying on the server.")
    @commands.has_permissions(manage_guild=True)
    async def spy(self, ctx, mode: int = None):
        desc = "**Something went wrong...**"
        enabled = "**Something went wrong...**"
        with open("db/guilds.json", "r") as f:
            data = json.load(f)
        if mode == 1:
            desc = "editing"
            data[str(ctx.guild.id)]["spy_edit"] = not data[str(ctx.guild.id)]["spy_edit"]
            enabled = data[str(ctx.guild.id)]["spy_edit"]
        elif mode == 2:
            desc = "deleting"
            data[str(ctx.guild.id)]["spy_delete"] = not data[str(ctx.guild.id)]["spy_delete"]
            enabled = data[str(ctx.guild.id)]["spy_edit"]
        elif mode is None:
            desc = "editing and deleting"
            data[str(ctx.guild.id)]["spy_delete"] = not data[str(ctx.guild.id)]["spy_delete"]
            data[str(ctx.guild.id)]["spy_edit"] = not data[str(ctx.guild.id)]["spy_edit"]
            enabled = data[str(ctx.guild.id)]["spy_edit"]
        embed = discord.Embed(
            title="Spy",
            description=f"Spying is now {enabled} for {desc} messages.",
            color=discord.Color.green(),
        )
        await ctx.send(embed=embed)
        with open("db/guilds.json", "w") as f:
            json.dump(data, f, indent=4)

    @commands.command(name="spy-channel")
    @commands.has_permissions(manage_guild=True)
    async def spy_channel(self, ctx, channel: discord.TextChannel):
        with open("db/guilds.json", "r") as f:
            data = json.load(f)
        data[str(ctx.guild.id)]["spy_channel"] = channel.id
        await ctx.send(f"Spy channel set to {channel.mention}.")
        with open("db/guilds.json", "w") as f:
            json.dump(data, f, indent=4)


async def setup(bot):
    await bot.add_cog(Spy(bot))

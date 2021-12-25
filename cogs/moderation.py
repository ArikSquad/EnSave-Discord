# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2021 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------

import discord
from discord.ext import commands


class Moderation(commands.Cog, name="Moderation", description="Moderation Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='Kick')
    @commands.has_permissions(kick_members=True)
    async def kick(self, context, member: discord.Member, *, reason="Not specified"):
        """
        Kick a user out of the server.
        """
        if member.guild_permissions.administrator:
            embed = discord.Embed(
                title="Error!",
                description="User has Admin permissions.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
        else:
            try:
                await member.kick(reason=reason)  # kicks the member with reason
                embed = discord.Embed(
                    title="User Kicked!",
                    description=f"**{member}** was kicked by **{context.message.author}**!",
                    color=0x42F56C
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await context.send(embed=embed)
                try:
                    await member.send(
                        f"You were kicked by **{context.message.author}**!\nReason: {reason}"
                    )
                except:
                    pass
            except:
                embed = discord.Embed(
                    title="Error!",
                    description="An error occurred while trying to kick the user. "
                                "Make sure my role is above the role of the user you want to kick.",
                    color=0xE02B2B
                )
                await context.message.channel.send(embed=embed)

    @commands.command(name="Nick")
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, context, member: discord.Member, *, nickname=None):
        """
        Change the nickname of a user on a server.
        """
        try:
            await member.edit(nick=nickname)
            embed = discord.Embed(
                title="Changed Nickname!",
                description=f"**{member}'s** new nickname is **{nickname}**!",
                color=0x42F56C
            )
            await context.send(embed=embed)
        except:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to change the nickname of the user. "
                            "Make sure my role is above the role of the user you want to change the nickname.",
                color=0xE02B2B
            )
            await context.message.channel.send(embed=embed)

    @commands.command(name="Ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, context, member: discord.Member, *, reason="Not specified"):
        """
        Bans a user from the server.
        """
        try:
            if member.guild_permissions.administrator:
                embed = discord.Embed(
                    title="Error!",
                    description="User has Admin permissions.",
                    color=0xE02B2B
                )
                await context.send(embed=embed)
            else:
                await member.ban(reason=reason)
                embed = discord.Embed(
                    title="User Banned!",
                    description=f"**{member}** was banned by **{context.message.author}**!",
                    color=0x42F56C
                )
                embed.add_field(
                    name="Reason:",
                    value=reason
                )
                await context.send(embed=embed)
                await member.send(f"You were banned by **{context.message.author}**!\nReason: {reason}")
        except:
            embed = discord.Embed(
                title="Error!",
                description="An error occurred while trying to ban the user. "
                            "Make sure my role is above the role of the user you want to ban.",
                color=0xE02B2B
            )
            await context.send(embed=embed)

    @commands.command(name="Warn")
    @commands.has_permissions(manage_messages=True)
    async def warn(self, context, member: discord.Member, *, reason="Not specified"):
        """
        Warns a user in his private messages.
        """
        embed = discord.Embed(
            title="User Warned!",
            description=f"**{member}** was warned by **{context.message.author}**!",
            color=0x42F56C
        )
        embed.add_field(
            name="Reason:",
            value=reason
        )
        await context.send(embed=embed)
        await member.send(f"You were warned by **{context.message.author}**!\nReason: {reason}")

    @commands.command(name="Purge", aliases=["clear", "vanish"])
    @commands.has_permissions(manage_messages=True, manage_channels=True)
    async def purge(self, context, amount):
        """
        Delete a number of messages.
        """
        try:
            amount = int(amount)
        except:
            embed = discord.Embed(
                title="Error!",
                description=f"`{amount}` is not a valid number.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        if amount < 1:
            embed = discord.Embed(
                title="Error!",
                description=f"`{amount}` is not a valid number.",
                color=0xE02B2B
            )
            await context.send(embed=embed)
            return
        purged_messages = await context.message.channel.purge(limit=amount)
        embed = discord.Embed(
            title="Chat Cleared!",
            description=f"**{context.message.author}** cleared **{len(purged_messages)}** messages!",
            color=0x42F56C
        )
        await context.send(embed=embed)


def setup(bot):
    bot.add_cog(Moderation(bot))

# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2021-2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import random

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

from utils import utility, db


class Misc(commands.Cog, description="Random commands"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.ctx_menu = app_commands.ContextMenu(
            name='Resend',
            callback=self.resend_context_menu,
        )
        self.bot.tree.add_command(self.ctx_menu)

    async def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu.name, type=self.ctx_menu.type)

    @app_commands.checks.has_permissions(send_messages=True)
    async def resend_context_menu(self, interaction: discord.Interaction, message: discord.Message) -> None:
        await interaction.response.defer(ephemeral=True)
        if not message.content:
            return await interaction.followup.send("You can't resend an empty message")
        channel: discord.TextChannel = interaction.channel
        webh = await channel.create_webhook(name=f'Resender', reason='Resend Context Menu')
        async with aiohttp.ClientSession() as session:
            webhook: discord.Webhook = discord.Webhook.from_url(webh.url, session=session)
            msg: discord.WebhookMessage = await webhook.send(message.content, username=message.author.name,
                                                             avatar_url=message.author.avatar.url
                                                             if message.author.avatar.url
                                                             else self.bot.user.avatar.url,
                                                             wait=True)
        await interaction.followup.send(f'Successfully resent message: [Here]({msg.jump_url}) ',)
        await webh.delete(reason='Resend Context Menu ended')

    @app_commands.command(name="dog", description="Posts a fun dog picture in the chat!")
    async def dog(self, interaction: discord.Interaction):
        title_text = "Dog" if random.randint(1, 2) == 1 else "Doggo"

        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://random.dog/woof.json') as r:
                data = await r.json()
                embed = discord.Embed(
                    title=title_text,
                    color=discord.Color.from_rgb(48, 50, 54)
                )
                embed.set_image(url=data['url'])
                await interaction.response.send_message(embed=embed)

    @app_commands.command(name="invite-bot", description='Get the invite link of the bot.')
    async def invite_bot(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title='Info',
            description=f'Invite me by clicking '
                        f'[here](https://discord.com/api/oauth2/authorize?client_id='
                        f'812808865728954399&permissions=8&scope=bot%20applications.commands).',
            color=discord.Color.from_rgb(48, 50, 54)
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='redeem', description="Redeem a code for a reward!")
    async def redeem(self, interaction: discord.Interaction, code: str):
        if not db.get_user_premium(interaction.user.id):
            keys = db.get_codes()

            success = False
            if (code,) in keys:
                success = True
                db.remove_code(code)

            if success:
                try:
                    utility.set_premium(interaction.user.id, True)
                except KeyError:
                    await interaction.response.send_message("Hey, please contact ArikSquad#6222 to get your premium, "
                                                            "something went wrong when giving automatically.")
                embed = discord.Embed(
                    title="Success!",
                    description=f"You have redeemed {code}!",
                    color=discord.Color.from_rgb(48, 50, 54)
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                embed = discord.Embed(
                    title="Error",
                    description=f"{interaction.user.mention} You have entered an invalid code!",
                    color=discord.Color.from_rgb(48, 50, 54)
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="Error",
                description=f"{interaction.user.mention} You are already a premium access!",
                color=discord.Color.from_rgb(48, 50, 54)
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Misc(bot))

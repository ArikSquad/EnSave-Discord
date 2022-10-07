# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2021-2022 MikArt
# Released under the Apache License 2.0
#
# -----------------------------------------------------------
import os

import discord
import mcstatus
from aiohttp import request
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
apikey = os.getenv('HYPIXELAPI')


class Minecraft(commands.Cog, description="Minecraft tools"):
    def __init__(self, bot):
        self.bot = bot

    # Command to get information about a Minecraft server
    @app_commands.command(name="mcserver", description="Get the status of a Java Minecraft server.")
    async def mcserver(self, interaction: discord.Interaction, server: str):
        try:
            status = mcstatus.JavaServer.lookup(server).status()
            player = discord.Embed(title=f"Minecraft Server Status: {server}",
                                   description="Server is online",
                                   color=0x00ff00)
            player.add_field(name="Players", value=f"{status.players.online}/{status.players.max}")
            player.add_field(name="Version", value=status.version.name, inline=False)
            player.add_field(name="Protocol", value=status.version.protocol, inline=False)
            player.add_field(name="Description", value=status.description, inline=False)
            await interaction.response.send_message(embed=player)
        except IOError:
            offline = discord.Embed(title=f"Minecraft Server Status: {server}",
                                    description=f"Server is offline.",
                                    color=discord.Color.from_rgb(48, 50, 54))
            await interaction.response.send_message(embed=offline)

    # Command to get data about Hypixel Bedwars players
    @app_commands.command(name="bedwars", description="Get the status of Hypixel Bedwars player.")
    async def hypixel_bedwars(self, interaction: discord.Interaction, username: str):
        url = f"https://api.hypixel.net/player?key={apikey}&name=" + username

        async with request("GET", url, headers={}) as response:
            if response.status == 200:
                data = await response.json()

                games_played = (data['player']['stats']["Bedwars"]["games_played_bedwars"])
                losses = (data['player']['stats']['Bedwars']["losses_bedwars"])
                wins = (data['player']['stats']['Bedwars']["wins_bedwars"])
                final_kills = (data['player']['stats']["Bedwars"]["final_kills_bedwars"])
                beds_broken = (data['player']['stats']["Bedwars"]["beds_broken_bedwars"])
                beds_lost = (data['player']['stats']["Bedwars"]["beds_lost_bedwars"])
            else:
                return await interaction.response.send_message("This command could not be executed. "
                                                               "Most likely due ratelimit.", ephemeral=True)

        embed = discord.Embed(title=f"{username} Bedwars Stats", color=discord.Color.from_rgb(48, 50, 54))
        embed.add_field(name="Games Played", value=f"{games_played} games", inline=False)
        embed.add_field(name="Losses", value=f"{losses} losses", inline=False)
        embed.add_field(name="Wins", value=f"{wins} wins", inline=False)
        embed.add_field(name="Final Kills", value=f"{final_kills} final kills", inline=False)
        embed.add_field(name="Beds Broken", value=f"{beds_broken} beds broken", inline=False)
        embed.add_field(name="Beds Lost", value=f"{beds_lost} beds lost", inline=False)
        embed.set_thumbnail(url="https://minotar.net/helm/" + username)
        await interaction.response.send_message(embed=embed)

    # Command to get a Minecraft user's skin
    @app_commands.command(name="skin", description="Get a Minecraft user skin.")
    async def get_skin(self, interaction: discord.Interaction, username: str):
        embed = discord.Embed(title=f"{username}'s skin",
                              description=f"Loading the skin of {username}...",
                              color=discord.Color.from_rgb(48, 50, 54))
        embed.set_thumbnail(url="https://minotar.net/helm/" + username)
        embed.set_image(url="https://minotar.net/armor/body/" + username)
        await interaction.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Minecraft(bot))

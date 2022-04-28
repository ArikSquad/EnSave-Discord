# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import os

import discord
import mcstatus
from aiohttp import request
from better_profanity import profanity
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
apikey = os.getenv('HYPIXELAPI')


class Minecraft(commands.Cog, description="Minecraft tools"):
    EMOJI = "🎮"

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="mcstatus", aliases=["mcs"], help="Get the status of a Java Minecraft server.")
    async def mcstatus(self, ctx, server: str):
        try:
            status = mcstatus.JavaServer.lookup(server).status()
            player = discord.Embed(title=f"Minecraft Server Status: {profanity.censor(server)}",
                                   description="Server is online",
                                   color=0x00ff00)
            player.add_field(name="Players", value=f"{status.players.online}/{status.players.max}")
            player.add_field(name="Version", value=status.version.name, inline=False)
            player.add_field(name="Protocol", value=status.version.protocol, inline=False)
            player.add_field(name="Description", value=status.description, inline=False)
            await ctx.send(embed=player)
        except IOError:
            offline = discord.Embed(title=f"Minecraft Server Status: {profanity.censor(server)}",
                                    description=f"Server is offline.",
                                    color=0xFF0000)
            await ctx.send(embed=offline)

    @commands.command(name="bedwars", aliases=["bw"], help="Get the status of Hypixel Bedwars player.")
    async def hypixel_bedwars(self, ctx, username):
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
                return await ctx.send("This command could not be executed. Try again later\n"
                                      "ERROR: RATELIMIT")

        embed = discord.Embed(title=f"{username} Bedwars Stats", color=discord.Color.orange())
        embed.add_field(name="Games Played", value=f"{games_played} games", inline=False)
        embed.add_field(name="Losses", value=f"{losses} losses", inline=False)
        embed.add_field(name="Wins", value=f"{wins} wins", inline=False)
        embed.add_field(name="Final Kills", value=f"{final_kills} final kills", inline=False)
        embed.add_field(name="Beds Broken", value=f"{beds_broken} beds broken", inline=False)
        embed.add_field(name="Beds Lost", value=f"{beds_lost} beds lost", inline=False)
        embed.set_thumbnail(url="https://minotar.net/helm/" + username)
        await ctx.send(embed=embed)

    @commands.command(name="skin", aliases=["mcskin", "minecraftskin"], help="Get the skin of a player.")
    async def get_skin(self, ctx, username: str):
        embed = discord.Embed(title=f"{username}'s skin",
                              description=f"Loading the skin of {username}...",
                              color=discord.Color.orange())
        embed.set_thumbnail(url="https://minotar.net/helm/" + username)
        embed.set_image(url="https://minotar.net/armor/body/" + username)
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Minecraft(bot))

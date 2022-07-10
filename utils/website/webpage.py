# -----------------------------------------------------------
# This is a discord bot by ArikSquad and you are viewing the source code of it.
#
# (C) 2022 MikArt
# Released under the CC BY-NC 4.0 (BY-NC 4.0)
#
# -----------------------------------------------------------
import asyncio
import os

from discord.ext import ipc
from dotenv import load_dotenv
from quart import Quart, render_template, redirect, url_for, request, flash
from quart_discord import DiscordOAuth2Session

from utils import db

app = Quart(__name__)

load_dotenv()
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['DISCORD_CLIENT_ID'] = os.getenv('CLIENT_ID')
app.config['DISCORD_CLIENT_SECRET'] = os.getenv('CLIENT_SECRET')
app.config['DISCORD_REDIRECT_URI'] = "http://localhost:1201/callback"

ipc_client = ipc.Client(secret_key=os.getenv('SECRET_KEY'))
discord = DiscordOAuth2Session(app)


@app.route('/')
async def index():
    return await render_template("index.html", authorized=await discord.authorized)


@app.route('/login')
async def login():
    return await discord.create_session()


@app.route('/logout')
async def logout():
    discord.revoke()
    return redirect(url_for("index"))


@app.route("/callback")
async def callback():
    try:
        await discord.callback()
    except Exception:
        pass

    return redirect(url_for("dashboard"))


@app.route("/dashboard")
async def dashboard():
    if not await discord.authorized:
        return redirect(url_for("login"))

    guild_count = await ipc_client.request("get_guild_count")
    bot_guilds = await ipc_client.request("get_guilds")
    user_guilds = await discord.fetch_guilds()

    guilds = []
    for guild in user_guilds:
        if guild.permissions.administrator:
            guild.class_color = "green-border" if guild.id in bot_guilds else "red-border"
            guilds.append(guild)

    guilds.sort(key=lambda x: x.class_color == "red-border")
    name = (await discord.fetch_user()).name
    return await render_template("selector.html", guild_count=guild_count, guilds=guilds, username=name)


@app.route("/dashboard/<int:guild_id>")
async def dashboard_server(guild_id):
    if not await discord.authorized:
        return redirect(url_for("login"))

    return redirect(url_for(f"dashboard_server_information", guild_id=guild_id))


@app.route("/dashboard/<int:guild_id>/information")
async def dashboard_server_information(guild_id):
    if not await discord.authorized:
        return redirect(url_for("login"))

    guild = await ipc_client.request("get_guild", guild_id=guild_id)
    user_guilds = await discord.fetch_guilds()

    accessible = False
    for gld in user_guilds:
        if gld.permissions.administrator and gld.id == guild_id:
            accessible = True
            break

    if accessible:
        if guild is None:
            return redirect(
                f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}'
                f'&scope=bot&permissions=8%20applications.command&guild_id={guild_id}'
                f'&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}')

        return await render_template("information.html", guild_name=guild["name"], current_prefix=guild["prefix"],
                                     guild_member_count=guild["member_count"],
                                     name=get_user_name, guild_id=guild["id"])
    else:
        return redirect(url_for("dashboard"))


@app.route("/dashboard/<int:guild_id>/customization", methods=["GET", "POST"])
async def dashboard_server_customization(guild_id):
    if not await discord.authorized:
        return redirect(url_for("login"))

    guild = await ipc_client.request("get_guild", guild_id=guild_id)
    user_guilds = await discord.fetch_guilds()

    accessable = False
    for gld in user_guilds:
        if gld.permissions.administrator and gld.id == guild_id:
            accessable = True
            break

    if accessable:
        if request.method == 'POST':
            form = await request.form
            prefix = form["prefix"]

            if len(prefix) != 0:
                db.set_guild_prefix(guild_id, prefix)
                await flash(f'Changed prefix to {prefix}', category='success')
                await asyncio.sleep(1)
                return redirect(url_for("dashboard_server_customization", guild_id=guild_id))

        if guild is None:
            return redirect(
                f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}'
                f'&permissions=8&scope=bot%20applications.commands&guild_id={guild_id}'
                f'&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}')

        return await render_template("customization.html", server_name=guild["name"],
                                     current_prefix=guild["prefix"], guild_id=guild_id)
    else:
        return redirect(url_for("dashboard"))


@app.route("/dashboard/<int:guild_id>/analytics")
async def dashboard_server_analytics(guild_id):
    if not await discord.authorized:
        return redirect(url_for("login"))

    guild = await ipc_client.request("get_guild", guild_id=guild_id)
    user_guilds = await discord.fetch_guilds()

    accessible = False
    for gld in user_guilds:
        if gld.permissions.administrator and gld.id == guild_id:
            accessible = True
            break

    if accessible:
        if guild is None:
            return redirect(
                f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}'
                f'&scope=bot&permissions=8&guild_id={guild_id}'
                f'&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}')

        return await render_template("analytics.html", server_name=guild["name"], current_prefix=guild["prefix"],
                                     guild_id=guild_id)
    else:
        return redirect(url_for("dashboard"))


@app.route("/dashboard/<int:guild_id>/settings")
async def dashboard_server_settings(guild_id):
    if not await discord.authorized:
        return redirect(url_for("login"))

    guild = await ipc_client.request("get_guild", guild_id=guild_id)
    user_guilds = await discord.fetch_guilds()

    accessible = False
    for gld in user_guilds:
        if gld.permissions.administrator and gld.id == guild_id:
            accessible = True
            break

    if accessible:
        if guild is None:
            return redirect(
                f'https://discord.com/oauth2/authorize?&client_id={app.config["DISCORD_CLIENT_ID"]}'
                f'&scope=bot&permissions=8&guild_id={guild_id}'
                f'&response_type=code&redirect_uri={app.config["DISCORD_REDIRECT_URI"]}')

        return await render_template("settings.html", server_name=guild["name"], current_prefix=guild["prefix"],
                                     guild_id=guild_id)
    else:
        return redirect(url_for("dashboard"))


@app.route("/commands")
async def commands():
    return await render_template("commands.html")


async def get_user_name(member_id):
    user = await ipc_client.request("get_user_name", member_id=member_id)
    if user is None:
        return member_id
    else:
        return user["name"]

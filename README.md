
<h1 align="center">
  <br>
  <br>
  EnSave Discord
  <br>
</h1>

<h4 align="center">True bot for everything you need from a bot.</h4>

<p align="center">
  <a href="https://discord.gg/Z5N5AWJmrA">
    <img src="https://discordapp.com/api/guilds/770634445370687519/widget.png?style=shield" alt="Discord Server">
  </a>

  <a href="https://www.patreon.com/ariksquad">
    <img src="https://img.shields.io/badge/Support-EnSave-red.svg" alt="Support EnSave on Patreon!">
  </a>
</p>
<p align="center">

 <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10-blue.svg">
  </a>
   <a href="https://github.com/nextcord/nextcord/">
     <img src="https://img.shields.io/badge/discord-py-blue.svg" alt="discord-py">
  <a href="https://creativecommons.org/licenses/by-nc/4.0/">
    <img src="https://img.shields.io/static/v1?label=license&message=BY-NC%204.0&color=orange&logo=creative%20commons&logoColor=white">
  <a href="https://twitter.com/intent/tweet?text=Wow:&url=https%3A%2F%2Fgithub.com%2FArikSquad%2FEnSave-Discord">
  </a>
  </a>
</a>
</p>

<p align="center">
  <a href="#overview">Overview</a>
  •
  <a href="#installation">Installation</a>
  •
  <a href="https://docs.mikart.eu">Documentation</a>
  •
  <a href="https://discord.gg/Z5N5AWJmrA">Community</a>
  •
  <a href="#license">License</a>
</p>


# Overview
This is an open-source discord bot developed by [ArikSquad](https://github.com/Ariksquad) and [Mhilkos](https://github.com/Mhilkos).
We also have documented files in this project, so feel free to check the files and see the documentation over there!
EnSave uses discord.py library which has been unarchived. If you would like to use this as your own bot, please give us some credit.

# Installation
1. Clone this repository using this command:
```commandline
git clone https://github.com/ArikSquad/EnSave-Discord.git
```
2. Open Command Prompt or Terminal. Then go into the folder with this command: 
```commandline
cd EnSave-Discord
 ```
3. Then install requirements in your terminal. This is very easy and done by this command:
```commandline
python3 -m pip install -r requirements.txt
```
6. After all that you should create a file named .env and put this inside it, but change "(your token)" to your discord bot token.
```env
TOKEN="(your token)"

MUSIC="(your lavalink ip)"
MUSIC_PASSWORD="(your lavalink password)"
HYPIXELAPI="(your hypixel api key)"

CLIENT_ID="(you only need this for dashboard)"
CLIENT_SECRET="(you only need this for dashboard)"
SECRET_KEY="(you only need this for dashboard)"
LOGIN_URL="(you only need this for dashboard)"
```
7. Good! Now you can run the bot by opening a new terminal and running this command:
```commandline
python3 main.py
```
8. If you want to use Music commands you need to follow [this](https://github.com/PythonistaGuild/Wavelink#lavalink-installation) guide
9. If you need more help with this then feel free to join our discord server. [Click here](https://discord.gg/WKTcnb86b7) to join the support server.

## Setupping a database for the bot
1. You should download a database browser, like [this](https://sqlitebrowser.org/).
2. Create a database.db so it will be like data/db/database.db
3. Use these sql commands to create tables:
```sql
CREATE TABLE "code" (
	"secret"	TEXT UNIQUE,
	"messageID"	INTEGER
);
CREATE TABLE "guild" (
	"guildID"	INTEGER UNIQUE,
	"prefix"	TEXT DEFAULT '.',
	"spy"	INTEGER DEFAULT 0,
	"channel"	INTEGER
);
CREATE TABLE "user" (
	"userID"	INTEGER UNIQUE,
	"premium"	INTEGER DEFAULT 0
);
``` 

## Reporting a Vulnerability or an Issue

If you found any vulnerabilities or issues please open an issue at the [Issues](https://github.com/ArikSquad/EnSave-Discord/issues) tab.
 
# License
This work is licensed under the [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/). To view a copy of this license, visit http://creativecommons.org/licenses/by-nc/4.0/ or send a letter to Creative Commons, PO Box 1866, Mountain View, CA 94042, USA. You are allowed to fork the project and distribute it, if you give credit. You may not sell any code protected by the license. Not all source files are protected by this license - Some third party libraries may be under different copyright.


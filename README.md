
<h1 align="center">
  <br>
  <br>
  EnSave Discord
  <br>
</h1>

<h4 align="center">True bot everything you need from a bot.</h4>

<p align="center">
  <a href="https://discord.gg/mikart">
    <img src="https://discordapp.com/api/guilds/770634445370687519/widget.png?style=shield" alt="Discord Server">
  </a>

  <a href="https://www.patreon.com/ariksquad">
    <img src="https://img.shields.io/badge/Support-EnSave-red.svg" alt="Support EnSave on Patreon!">
  </a>
</p>
<p align="center">

 <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10-blue.svg" alt="python">
  </a>
   <a href="https://github.com/Rapptz/discord.py">
     <img src="https://img.shields.io/badge/discord-py-blue.svg" alt="discord-py">
  <a href="https://www.apache.org/licenses/LICENSE-2.0">
    <img src="https://img.shields.io/badge/License-Apache_2.0-olive.svg" alt="license">
  <a href="https://twitter.com/intent/tweet?text=This%20is%20amazing:&url=https%3A%2F%2Fgithub.com%2FArikSquad%2FEnSave-Discord">
    <img src="https://img.shields.io/badge/tweet-us-blue.svg" alt="discord-py">
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
This is an open-source discord bot developed by [ArikSquad](https://github.com/Ariksquad).
We also have some documented files in this project, so feel free to check the files and see the documentation over there!
EnSave uses the latest discord.py library. If you would like to use this as your template for your bot, please add mention us.

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
```
7. Good! Now you can run the bot by opening a new terminal and running this command:
```commandline
python3 main.py
```
8. If you want to use Music commands you need to follow [this](https://github.com/PythonistaGuild/Wavelink#lavalink-installation) guide
9. If you need more help with this then feel free to join our discord server. [Click here](https://discord.gg/WKTcnb86b7) to join the support server.

## Setupping a database for the bot
1. You should download a database browser, like [this](https://sqlitebrowser.org/).
2. Create a database.db in the directory /data/db/
3. The database should be automatically created when you run the bot.
<br><br><br> **If something goes wrong use these SQL commands**: 
```sql
CREATE TABLE "code" (
	"secret"	TEXT UNIQUE
);
CREATE TABLE "guild" (
	"guildID"	INTEGER UNIQUE,
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
This work is licensed under the [Apache License](https://www.apache.org/licenses/LICENSE-2.0), you may not use this file except in compliance with the License. You may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0 Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
<br>
<b>Not all source files are protected by this license - Some third party libraries may be under different copyright.</b>


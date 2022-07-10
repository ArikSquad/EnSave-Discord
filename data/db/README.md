## Setupping a database for the bot
1. You should download a database browser, like [this](https://sqlitebrowser.org/).
2. Create a database.db in this directory.
3. Use these sql commands to create tables:
```sql
CREATE TABLE "code" (
	"secret"	TEXT UNIQUE
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
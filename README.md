# UxRepostBot [Legacy]
Legacy version of UxRepostBot - can repost messages from telegram channel to chat/contact WITHOUT channel admin rights (works with some bad practice, but stable).
New version (with requirement admin channel rights) will be released soon.

# Installation
1. Clone repo
1. Install dependencies from requirements.txt (like pip install or with your virtualenv/conda environment)
1. You **MUST** save last telegram post_id from channel to `data.txt`, otherwise bot cant find start point for check new posts! (can find with telegram web or traffic sniffer)
1. Run python3 main.py (or write .sh script for your needs)

# Config
- `PREFIX` - working directory for pid file
- `LOG_FORMAT` - default python logger format string
- `LOG_LEVEL` - min level to log
- `BEEP_TIME` - time for check user count in main channel (in mins)
- `CHAN_FROM` - telegram channel id (from)
- `ID_TO` - telegram chat id or user id (to, you must add bot to chat or write first to him (if single contact))
- `BOT_ID` - telegram bot id (numbers before semicolon in 123456:abce123fgbji...)
- `SECRET_TOKEN` - telegram bot token (text after semicolon 123456:abce123fgbji...)
- `HEADERS` - headers for HTTPS requests

# Requirements
Works only on *nix systems, because app using pidfile library (for autorestart with cron if crashed).
On windows you can just remove it or use through Windows Subsystem for Linux (WSL/LXSS) - it's tested and worked stable.


# Changelog
## v1.1 - 26.06.2017
Public release, update logger, update config, add feature to watch for user counter in channel. 

## v1.0 - march 2017
Add fix for freeze state when some post was deleted and bot stuck at some post id.

## v0.9 - winter 2017
First beta.

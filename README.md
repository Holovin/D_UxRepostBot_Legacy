# UxRepostBot [Legacy]
Legacy version of UxRepostBot - can repost messages from telegram channel to chat/contact WITHOUT channel admin rights (works with some bad practice, but stable).
New version (with requirement admin channel rights) will be released soon.

## Installation
1. Clone repo
1. Install dependencies from requirements.txt (like pip install or with your virtualenv/conda environment)
1. You **MUST** save last telegram post_id from channel to `data.txt`, otherwise bot cant find start point for check new posts! (can find with telegram web or traffic sniffer)
1. Run python3 main.py (or write .sh script for your needs)

## Config
### System vars
- `PREFIX` - working directory for pid file
- `LOG_FORMAT` - default python logger format string
- `LOG_LEVEL` - min level to log
- `TIMEZONE` - timezone for logfile and check timers

### Telegram vars
- `CHAN_FROM` - telegram channel id (from)
- `ID_TO` - telegram chat id or user id (to, you must add bot to chat or write first to him (if single contact))
- `LOG_TO` - telegram user id to send init message (and another important logs in future)

### Check time vars
- `BEEP_TIME` - time for check user count in main channel (in mins)
- `USER_COUNT_CHECK_TIMER` - minutes between check user counters
- `USER_MIN_NEW` - minimal new users to display (for `USER_COUNT_CHECK_TIMER` minutes)
- `USER_MIN_DELTA` - minimal users delta changes to display (for `USER_COUNT_CHECK_TIMER` minutes)

### Bot data
- `WORDS_FILE` = path to file with text which append to count messages

### Telegram bots
- `BOT_ID` - telegram bot id (numbers before semicolon in 123456:abce123fgbji...)
- `SECRET_TOKEN` - telegram bot token (text after semicolon 123456:abce123fgbji...)

### Other
- `HEADERS` - headers for HTTPS requests

## Requirements
Works only on *nix systems, because app using pidfile library (for autorestart with cron if crashed).
On windows you can just remove it or use through Windows Subsystem for Linux (WSL/LXSS) - it's tested and worked stable.

## Changelog
### v1.2a - 02.07.2017
Day results, force state param, send copy of mesgs and format error fixes.

### v1.2 - 29.06.2017
Fix user counter, timezone support and logger update.

### v1.1 - 26.06.2017
Public release, update logger, update config, add feature to watch for user counter in channel. 

### v1.0 - march 2017
Add fix for freeze state when some post was deleted and bot stuck at some post id.

### v0.9 - winter 2017
First beta.

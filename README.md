# UxRepostBot [Legacy]
Legacy version of UxRepostBot - channel stats counter & announcer.

Since new api update(october 2017) CAN NOT repost messages from telegram channel to chat/contact WITHOUT channel admin rights (works with some bad practice, but stable). New version (with requirement admin channel rights) will be released soon.

## Installation
1. Clone repo
1. Install dependencies from requirements.txt (like pip install or with your virtualenv/conda environment)
1. Run python3 main.py (or write .sh script for your needs)

## Config
### System vars
- `LOG_FORMAT` - default python logger format string
- `LOG_LEVEL` - min level to log
- `TIMEZONE` - timezone for logfile and check timers

For database config see table structure in `db_models.py` file.

### Telegram bots
- `BOT_ID` - telegram bot id (numbers before semicolon in 123456:abce123fgbji...)
- `SECRET_TOKEN` - telegram bot token (text after semicolon 123456:abce123fgbji...)

### Other
- `HEADERS` - headers for HTTPS requests

## Changelog
### v1.3 - 30.11.2017
Remove repost module, because telegram api now restrict 'shadow' reposts.
Fully rework stats module: multichannel support, save state to sqlite3 database, have much improvements. 

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

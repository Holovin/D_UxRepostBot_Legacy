import logging


class Config:
    LOG_FULL_PATH = 'log.txt'
    LOG_FORMAT = '%(module)-16s %(levelname)-8s [%(asctime)s] %(message)s'
    LOG_LEVEL = logging.INFO
    LOG_OUTPUT = True

    SQLITE_DB_FULL_PATH = 'settings.db'

    TIMEZONE = 'Europe/Minsk'

    BOT_ID = '263878562'
    SECRET_TOKEN = 'AAFEFFj5qY64Oc9XST_AYf9XlIUQZiUTWzM'

    HEADERS = {
        'Cache-Control': 'no-cache',
        'Expires': 'Thu, 01 Jan 1970 00:00:00 GMT',
        'Pragma': 'no-cache',
        'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:2.0b7) Gecko/20100101 Firefox/4.0b7'
    }

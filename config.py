import logging


class Config:
    PREFIX = './' # '/data/backend/ux_bot/'
    LOG_FORMAT = '%(levelname)-8s [%(asctime)s] %(message)s'
    LOG_LEVEL = logging.DEBUG
    TIMEZONE = 'Europe/Minsk'

    CHAN_FROM = '@'
    ID_TO = '1'
    LOG_TO = '1'

    USER_COUNT_CHECK_TIMER = 60
    USER_MIN_NEW = 5
    USER_MIN_DELTA = 10
    WORDS_FILE = 'words.txt'

    BOT_ID = '1'
    SECRET_TOKEN = 'A'

    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:2.0b7) Gecko/20100101 Firefox/4.0b7'}

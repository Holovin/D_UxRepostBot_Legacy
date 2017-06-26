import logging


class Config:
    PREFIX = './' # '/data/backend/ux_bot/'
    LOG_FORMAT = '%(levelname)-8s [%(asctime)s] %(message)s'
    LOG_LEVEL = logging.INFO

    BEEP_TIME = 20

    CHAN_FROM = '@'
    BOT_ID = '1'
    ID_TO = '-1'
    SECRET_TOKEN = '1'

    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:2.0b7) Gecko/20100101 Firefox/4.0b7'}

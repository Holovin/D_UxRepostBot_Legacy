# logger.py
# App logger initialization function
# r1

import logging
from logging.handlers import RotatingFileHandler
from config import Config


def logger_setup(log_file, loggers=None, touch_root=False):
    log_formatter = logging.Formatter(Config.LOG_FORMAT, datefmt='%Y/%m/%d %H:%M:%S')
    log_level = Config.LOG_LEVEL
    full_debug = Config.LOG_OUTPUT

    console = logging.StreamHandler()
    console.setLevel(log_level)
    console.setFormatter(log_formatter)

    root = logging.getLogger()

    if touch_root:
        root.setLevel(log_level)
        root.addHandler(logging.NullHandler())

        if full_debug:
            root.addHandler(console)
            root.info('Console output enabled')

    handler = RotatingFileHandler(log_file, backupCount=1, encoding='utf8')
    handler.setLevel(log_level)
    handler.setFormatter(log_formatter)
    handler.doRollover()

    if loggers:
        for logger_name in loggers:
            logger = logging.getLogger(logger_name)
            logger.setLevel(log_level)
            logger.addHandler(handler)
            logger.propagate = False

            if full_debug:
                logger.addHandler(console)
    else:
        root.warning('Empty loggers list')

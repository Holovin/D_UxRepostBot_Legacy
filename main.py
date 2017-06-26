#!/usr/bin/python3

import logging
import pidfile
import time

from logging.handlers import RotatingFileHandler
from pytz import timezone
from datetime import datetime, timedelta

from config import Config
from api import API
from data import Data

if __name__ == '__main__':
    with pidfile.PidFile(Config.PREFIX + 'pid'):
        # init
        logging.basicConfig(format=Config.LOG_FORMAT, level=Config.LOG_LEVEL)
        fmt = logging.Formatter(Config.LOG_FORMAT, datefmt='%Y-%m-%d')

        logger = logging.getLogger('ux_repost_bot_legacy')

        handler = RotatingFileHandler(filename=Config.PREFIX + 'log.txt', maxBytes=10000000, backupCount=5)
        handler.setFormatter(Config.LOG_FORMAT)
        handler.setLevel(Config.LOG_LEVEL)
        handler.setFormatter(fmt)

        logger.addHandler(handler)

        app = API(Config.BOT_ID, Config.SECRET_TOKEN, logger)
        data = Data(Config.PREFIX + 'data.txt')
        current_post_str_id = data.get()

        current_sleep_sec = 1
        freeze_count = 0

        last_time = datetime.now(timezone('Europe/Minsk')) - timedelta(minutes=Config.BEEP_TIME)
        current_total_users = 0

        # pre-check
        if not current_post_str_id.isdigit():
            logger.fatal('Wrong input data: %s.' % current_post_str_id)
            exit(1)

        current_post_int_id = int(current_post_str_id)

        # app.api_send_message(Config.ID_TO, '[INFO] UxRepostBot_legacy_v1.1 is up...')

        # main
        while True:
            logger.info('Read from: %d' % current_post_int_id)
            resp = app.api_forward_message(Config.ID_TO, Config.CHAN_FROM, 'False', str(current_post_int_id))

            if datetime.now(timezone('Europe/Minsk')) - last_time > timedelta(minutes=Config.BEEP_TIME):
                last_time = datetime.now(timezone('Europe/Minsk'))
                resp_users = app.api_get_chat_members_count(Config.CHAN_FROM)

                if resp_users:
                    new_total_users = resp_users.get('result')
                    delta = new_total_users - current_total_users

                    if delta != 0:
                        app.api_send_message(Config.ID_TO, 'UX Live подписок %d, изменения %+d.' % (new_total_users, delta))

                    logging.info('Users total: %d, changes %+d' % (new_total_users, delta))
                    current_total_users = new_total_users

                else:
                    logging.warning('Cant count users delta (err: empty response) ')
                    app.api_send_message(Config.ID_TO, '[WARN] Cant count users delta (err: empty response)')

            if resp:
                # send
                if API.api_check_success(resp):
                    logger.info('Post send ok: %d' % current_post_int_id)
                    current_post_int_id += 1
                    data.set(str(current_post_int_id))
                    time.sleep(1)
                    current_sleep_sec = 1

                # no post
                else:
                    logger.info('No new posts: %d' % current_post_int_id)
                    time.sleep(current_sleep_sec)

                    freeze_count += 1

                    # check skipped
                    if freeze_count > 5:
                        freeze_count = 0

                        for post_id in range(current_post_int_id + 1, current_post_int_id + 5):
                            logger.info('Unfreeze: %d' % post_id)
                            resp = app.api_forward_message(Config.ID_TO, Config.CHAN_FROM, 'False', str(post_id))
                            time.sleep(3)

                            if resp and API.api_check_success(resp):
                                current_post_int_id = post_id + 1
                                break

                    # slow timer
                    if current_sleep_sec < 60:
                        current_sleep_sec += 3

            # wrong network
            else:
                logger.info('Possible error...')
                time.sleep(600)

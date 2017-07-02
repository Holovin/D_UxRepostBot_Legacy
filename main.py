#!/usr/bin/python3

import logging
import random

import pidfile
import time

from logging.handlers import RotatingFileHandler
from pytz import timezone
from datetime import datetime, timedelta

from config import Config
from api import API
from data import Data


def random_line(file):
    line = next(file)

    for num, aline in enumerate(file):
        if random.randrange(num + 2):
            continue

        line = aline

    return line


if __name__ == '__main__':
    with pidfile.PidFile(Config.PREFIX + 'pid'):
        # init
        # logging.basicConfig(format=Config.LOG_FORMAT, level=Config.LOG_LEVEL)
        fmt = logging.Formatter(Config.LOG_FORMAT, datefmt=':%Y/%m/%d %H:%M:%S')

        logger = logging.getLogger('ux_repost_bot_legacy')

        handler = RotatingFileHandler(filename=Config.PREFIX + 'log.txt', maxBytes=10000000, backupCount=5)
        handler.setFormatter(Config.LOG_FORMAT)
        handler.setLevel(Config.LOG_LEVEL)
        handler.setFormatter(fmt)

        logger.propagate = False
        logger.addHandler(handler)

        app = API(Config.BOT_ID, Config.SECRET_TOKEN, logger)
        data = Data(Config.PREFIX + 'data.txt')
        current_post_str_id = data.get()

        current_sleep_sec = 1
        freeze_count = 0

        last_time = datetime.now(timezone(Config.TIMEZONE)) - timedelta(minutes=Config.USER_COUNT_CHECK_TIMER)
        total_users_current = 0
        current_stash_users = 0
        current_day_users = 0
        force_state = False

        # pre-check
        if not current_post_str_id.isdigit():
            logger.fatal('Wrong input data: {}.'.format(current_post_str_id))
            exit(1)

        current_post_int_id = int(current_post_str_id)

        # init
        total_users_current = app.api_get_chat_members_count(Config.CHAN_FROM).get('result')
        total_users_fresh = total_users_current

        # log
        if Config.LOG_TO:
            app.api_send_message(Config.LOG_TO, '[INFO] UxRepostBot legacy v1.2 is up...')

        # main
        while True:
            logger.info('Read from: {:d}'.format(current_post_int_id))
            resp = app.api_forward_message(Config.ID_TO, Config.CHAN_FROM, 'False', str(current_post_int_id))

            if datetime.now(timezone(Config.TIMEZONE)) - last_time > timedelta(minutes=Config.USER_COUNT_CHECK_TIMER):
                current_day = last_time.day
                last_time = datetime.now(timezone(Config.TIMEZONE))
                resp_users = app.api_get_chat_members_count(Config.CHAN_FROM)

                logger.info(
                    'Get user count: {}, last time: {}, currentDay: {}'.format(resp_users, last_time, current_day))

                if resp_users:
                    total_users_fresh = resp_users.get('result')

                    # update delta
                    new_users = total_users_fresh - total_users_current
                    current_stash_users += abs(new_users)

                    # reset day counter
                    if current_day == last_time.day:
                        current_day_users += new_users

                    else:
                        force_state = True

                    logger.info('New users {}, delta {}, today {}'.format(new_users, current_stash_users,
                                                                          current_day_users))

                    with open(Config.WORDS_FILE) as f:
                        random_text = random_line(f)

                    app.api_send_message(
                        Config.LOG_TO, '*UxLive stats* ({:%Y/%m/%d %H:%M:%S})\n'
                                       'Подписчиков: {:d}\n'
                                       'За последние {:d} минут: {:+d}\n'
                                       'За день: {:+d}\n'
                                       '\n'
                                       '{}'
                            .format(last_time,
                                    total_users_fresh,
                                    Config.USER_COUNT_CHECK_TIMER, new_users,
                                    current_day_users,
                                    random_text),
                        'markdown')

                    if (new_users >= Config.USER_MIN_NEW or current_stash_users >= Config.USER_MIN_DELTA) \
                            and total_users_current > 0 or force_state:
                        app.api_send_message(
                            Config.ID_TO, '*UxLive stats* ({:%Y/%m/%d %H:%M:%S})\n'
                                          'Подписчиков: {:d}\n'
                                          'За последние {:d} минут: {:+d}\n'
                                          'За день: {:+d}\n\n{}'
                                .format(last_time,
                                        total_users_fresh,
                                        Config.USER_COUNT_CHECK_TIMER, new_users,
                                        current_day_users,
                                        random_text),
                            'markdown')

                        logging.info('Users total: {}, changes {:+d}'.format(total_users_fresh, new_users))

                        current_stash_users = 0
                        force_state = False

                    # update after send or skip
                    total_users_current = total_users_fresh

                    # reset
                    if current_day != last_time.day:
                        current_day_users = 0

                else:
                    logging.warning('Cant count users delta (err: empty response) ')
                    app.api_send_message(Config.ID_TO, '[WARN] Cant count users delta (err: empty response)')

            if resp:
                # send
                if API.api_check_success(resp):
                    logger.info('Post send ok: %d'.format(current_post_int_id))
                    current_post_int_id += 1
                    data.set(str(current_post_int_id))
                    time.sleep(1)
                    current_sleep_sec = 1

                # no post
                else:
                    logger.info('No new posts: {:d}'.format(current_post_int_id))
                    time.sleep(current_sleep_sec)

                    freeze_count += 1

                    # check skipped
                    if freeze_count > 5:
                        freeze_count = 0

                        for post_id in range(current_post_int_id + 1, current_post_int_id + 5):
                            logger.info('Unfreeze: {}'.format(post_id))
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

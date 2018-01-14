#!/usr/bin/python3

import logging
import time

from pytz import timezone
from datetime import datetime, timedelta
from dateutil.parser import parse

from config import Config
from api import API
from helpers.db_connect import Database
from helpers.db_models import Settings
from helpers.logger import logger_setup


def get_amazing_date(timedelta: timedelta):
    hours_vars = ['час', 'часа', 'часов']
    minutes_vars = ['минуту', 'минуты', 'минут']

    # check hours
    hours = round(timedelta.seconds / 3600) % 20
    output = get_pretty_string_time(hours_vars, hours)

    if output:
        return output

    # check min
    minutes = round(timedelta.seconds / 60) % 20
    output = get_pretty_string_time(minutes_vars, minutes)

    if output:
        return output

    return 'последнее время'


def get_pretty_string_time(strings, timediff):
    if timediff > 0:
        # 1 минуту / час
        out = strings[0]

        # 2 3 4 минуты / часа
        if 1 < timediff < 5:
            out = strings[1]

        # 5 6 7 8 ... минут / часов
        elif timediff >= 5:
            out = strings[2]

        return '{} {}'.format(timediff, out)

    return ''


def str_to_time(data):
    if type(data) is str:
        return parse(data)

    return data


if __name__ == '__main__':
    # init
    LOGGER_NAME = 'ux_repost_bot_legacy'
    logger = logging.getLogger(LOGGER_NAME)
    logger_setup(Config.LOG_FULL_PATH, [LOGGER_NAME], True)

    app = API(Config.BOT_ID, Config.SECRET_TOKEN, logger)
    tz = timezone(Config.TIMEZONE)

    # db
    database = Database.get_db()
    database.connect()

    channels = []
    for channel in Settings.select():
        channel.stat_last_check_time = str_to_time(channel.stat_last_check_time)
        channel.write_last_time = str_to_time(channel.write_last_time)

        channels.append(channel)

    last_check_datetime = datetime.now(tz)

    while True:
        try:
            for channel in channels:
                logging.info('Check channel: {} (date check: {}, date write: {})'.format(channel.channel_name, channel.stat_last_check_time, channel.write_last_time))

                try:
                    result = app.api_get_chat_members_count(channel.channel_name)
                    last_check_datetime = datetime.now(tz)

                    if not result:
                        err = 'Cant count users delta for {} (err: empty response)'.format(channel.channel_name)
                        logging.warning(err)
                        app.api_send_message(channel.admin_to, err)
                        raise Exception('Empty result')

                except Exception as e:
                    logging.warning('{}\n{}'.format(e, err))
                    app.api_send_message(channel.admin_to, '{}\n{}'.format(e, err))
                    continue

                # new_users = total_users_fresh - total_users_current
                new_users_fresh = result.get('result')
                new_users = new_users_fresh - channel.stat_total_users

                # update period
                channel.stat_period_users += new_users

                # update delta
                channel.stat_delta_users += abs(new_users)

                # update day counter
                if channel.stat_last_check_time.day == last_check_datetime.day:
                    channel.stat_day_users += new_users

                ### send checks ###
                send_reason = ''
                send_force = False

                # uncomment for test purpose
                # send_force = True
                # send_reason = 'Test'

                if new_users_fresh >= channel.stat_max_users and new_users_fresh != channel.stat_total_users \
                        and new_users_fresh // channel.trigger_every_odd > channel.stat_max_users // channel.trigger_every_odd:
                    send_reason = '#get {}!'.format(new_users_fresh)
                    send_force = True

                elif channel.trigger_new_day and channel.stat_last_check_time.day != last_check_datetime.day:
                    send_reason = 'новый день'

                elif channel.stat_period_users >= channel.trigger_min_sub:
                    send_reason = 'подписки'

                elif channel.stat_period_users <= channel.trigger_min_unsub:
                    send_reason = 'отписки'

                elif channel.stat_delta_users >= channel.trigger_min_flow:
                    send_reason = 'поток'

                time_diff = datetime.now(tz) - channel.write_last_time

                logging.info('New users: {} (diff: {})\n'
                             'Trigger: {} (force? {})\n'
                             'Send diff: {}\n'.format(new_users_fresh, new_users, send_reason, send_force, time_diff))
                # send & reset stash
                if (time_diff >= timedelta(minutes=channel.write_ban_minutes) and send_reason != '') or send_force:
                    message = ('*Stats:* [{}](https://t.me/{}) ({:%Y/%m/%d %H:%M:%S})\n'
                               'Подписчиков: {:d}\n'
                               'За {}: {:+d}\n'
                               'За день: {:+d}\n'
                               'Поток: {:+d} [(?)](http://telegra.ph/Ux-Stats-11-30)\n'
                               'Триггер: {}\n'
                               '#uxstat'
                               .format(channel.channel_name, channel.channel_name[1:], last_check_datetime,
                                       new_users_fresh,
                                       get_amazing_date(datetime.now(tz) - channel.write_last_time), channel.stat_period_users,
                                       channel.stat_day_users,
                                       channel.stat_delta_users,
                                       send_reason
                                       )
                               )

                    if channel.admin_to != channel.print_to:
                        app.api_send_message(channel.admin_to, 'PREVIEW:\n\n{}'.format(message), 'markdown')

                    app.api_send_message(channel.print_to, message, 'markdown')

                    channel.write_last_time = datetime.now(tz)
                    channel.stat_delta_users = 0
                    channel.stat_period_users = 0

                ### post update ###
                # update total (not move above delta count line!)
                channel.stat_total_users = new_users_fresh

                # update max
                if new_users_fresh > channel.stat_max_users:
                    channel.stat_max_users = new_users_fresh

                # reset day stat if needed
                if channel.stat_last_check_time.day != last_check_datetime.day:
                    channel.stat_day_users = 0

                # update time
                channel.stat_last_check_time = datetime.now(tz)

                # save
                channel.save()
                time.sleep(2)

        except Exception as e:
            logging.warning('{}\n{}'.format(e, err))
            app.api_send_message(Settings.get(Settings.id == 1).admin_to, '{}\n{}'.format(e, err))

        finally:
            time.sleep(10)

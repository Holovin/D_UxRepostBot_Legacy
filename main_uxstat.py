#!/usr/bin/python3

import logging
import time

from logging.handlers import RotatingFileHandler

from pytz import timezone
from datetime import datetime, timedelta

from config import Config
from api import API
from helpers.db_connect import Database
from helpers.db_manager import Serve
from helpers.db_models import Settings


def get_amazing_date(timedelta: timedelta):
    hours_vars = ['час', 'часа', 'часов']
    minutes_vars = ['минуту', 'минуты', 'минут']

    # check hours
    hours = round(timedelta.seconds / 3600)
    output = get_pretty_string_time(hours_vars, hours)

    if output:
        return output

    # check min
    minutes = round(timedelta.seconds / 60)
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


if __name__ == '__main__':
    # Serve.create_tables(Database.get_db())
    # exit(99)

    # init
    root = logging.getLogger()
    root.addHandler(logging.NullHandler())

    fmt = logging.Formatter(Config.LOG_FORMAT, datefmt=':%Y/%m/%d %H:%M:%S')
    logger = logging.getLogger('ux_repost_bot_legacy')
    handler = RotatingFileHandler(filename='log.txt', maxBytes=10000000, backupCount=5)
    handler.setFormatter(Config.LOG_FORMAT)
    handler.setLevel(Config.LOG_LEVEL)
    handler.setFormatter(fmt)
    logger.propagate = True
    logger.setLevel(Config.LOG_LEVEL)
    logger.addHandler(handler)

    app = API(Config.BOT_ID, Config.SECRET_TOKEN, logger)

    # db
    database = Database.get_db()
    database.connect()

    channels = []
    for channel in Settings.select():
        channels.append({
            'id': channel.id,
            'name': channel.channel_name,
            'print_to': channel.print_to,
            'admin_to': channel.admin_to,
            'trigger_min_sub': channel.trigger_min_sub,
            'trigger_min_ubsub': channel.trigger_min_unsub,
            'trigger_min_flow': channel.trigger_min_flow,
            'trigger_every_odd': channel.trigger_every_odd,
            'trigger_new_day': channel.trigger_new_day,

            'stat_total_users': channel.stat_total_users,
            'stat_day_users': channel.stat_day_users,
            'stat_delta_users': channel.stat_delta_users,
            'stat_max_users': channel.stat_max_users,
            'stat_last_check_time': datetime.fromtimestamp(channel.stat_last_check_time, tz=timezone(Config.TIMEZONE)),

            'write_ban_minutes': channel.write_ban_minutes,
            'write_last_time': datetime.fromtimestamp(channel.write_last_time, tz=timezone(Config.TIMEZONE)),
        })

    last_check_datetime = datetime.now(timezone(Config.TIMEZONE))

    while True:
        try:
            for channel in channels:
                try:
                    result = app.api_get_chat_members_count(channel.get('name'))
                    last_check_datetime = datetime.now(timezone(Config.TIMEZONE))

                    if not result:
                        err = 'Cant count users delta for {} (err: empty response)'.format(channel.get('name'))
                        logging.warning(err)
                        app.api_send_message(channel.get('admin_to'), err)
                        raise Exception('Empty result')

                except Exception as e:
                    logging.warning('{}\n{}'.format(e, err))
                    app.api_send_message(channel.get('admin_to'), '{}\n{}'.format(e, err))
                    continue

                # new_users = total_users_fresh - total_users_current
                new_users_fresh = result.get('result')
                new_users = new_users_fresh - channel.get('stat_total_users')

                # update delta
                channel.update({'stat_delta_users': channel.get('stat_delta_users') + abs(new_users)})

                # update day counter
                if channel.get('stat_last_check_time').day == last_check_datetime.day:
                    channel.update({'stat_day_users': channel.get('stat_day_users') + new_users})

                ### send checks ###
                send_reason = ''
                send_force = False

                # uncomment for test purpose
                # send_force = True
                # send_reason = 'Test'

                if new_users_fresh != channel.get('stat_max_users') \
                        and new_users_fresh != channel.get('stat_total_users') \
                        and new_users_fresh % channel.get('trigger_every_odd') == 0:
                    send_reason = '#get {}!'.format(new_users_fresh)
                    send_force = True

                elif channel.get('stat_last_check_time').day != last_check_datetime.day:
                    send_reason = 'новый день'

                elif new_users >= channel.get('trigger_min_sub'):
                    send_reason = 'подписки'

                elif new_users <= channel.get('trigger_min_ubsub'):
                    send_reason = 'отписки'

                elif channel.get('stat_delta_users') >= channel.get('trigger_min_flow'):
                    send_reason = 'поток'

                # send & reset stash
                if ((datetime.now(timezone(Config.TIMEZONE)) - channel.get('write_last_time') >= timedelta(minutes=channel.get('write_ban_minutes')))
                        and send_reason != '') or send_force:

                    message = ('*Stats:* [{}](https://t.me/{}) ({:%Y/%m/%d %H:%M:%S})\n''Подписчиков: {:d}\n'
                               'За {}: {:+d}\n'
                               'За день: {:+d}\n'
                               'Поток: {:+d} [(?)](http://telegra.ph/Ux-Stats-11-30)\n'
                               'Триггер: {}\n'
                               '#uxstat'
                               .format(channel.get('name'), channel.get('name')[1:], last_check_datetime,
                                       new_users_fresh,
                                       get_amazing_date(datetime.now(timezone(Config.TIMEZONE)) - channel.get('write_last_time')),
                                       new_users,
                                       channel.get('stat_day_users'),
                                       channel.get('stat_delta_users'),
                                       send_reason
                               ))

                    app.api_send_message(channel.get('admin_to'), 'PREVIEW:\n\n{}'.format(message), 'markdown')
                    app.api_send_message(channel.get('print_to'), message, 'markdown')

                    channel.update({'write_last_time': datetime.now(timezone(Config.TIMEZONE))})
                    channel.update({'stat_delta_users': 0})

                ### post update ###
                # update total (not move above delta count line!)
                channel.update({'stat_total_users': new_users_fresh})

                # update max
                if new_users_fresh > channel.get('stat_max_users'):
                    channel.update({'stat_max_users': new_users_fresh})

                # reset day stat if needed
                if channel.get('stat_last_check_time').day != last_check_datetime.day and send_reason != '':
                    channel.update({'stat_day_users': 0})

                # update time
                channel.update({'stat_last_check_time': datetime.now(timezone(Config.TIMEZONE))})

                # save
                db_channel = Settings.get(Settings.id == channel.get('id'))

                if db_channel:
                    db_channel.stat_total_users = channel.get('stat_total_users')
                    db_channel.stat_day_users = channel.get('stat_day_users')
                    db_channel.stat_max_users = channel.get('stat_max_users')
                    db_channel.stat_delta_users = channel.get('stat_delta_users')

                    # any best way to drop THIS FUCKING USELESS MICROSECONDS?
                    db_channel.stat_last_check_time = str(int(channel.get('stat_last_check_time').timestamp()))
                    db_channel.write_last_time = str(int(channel.get('write_last_time').timestamp()))

                    db_channel.save()

                time.sleep(7)

        except Exception as e:
            logging.warning('{}\n{}'.format(e, err))
            app.api_send_message(Settings.get(Settings.id == 1).admin_to, '{}\n{}'.format(e, err))

        finally:
            time.sleep(30)

from peewee import *
from pytz import timezone
from datetime import datetime

from config import Config
from helpers.db_connect import Database


class BaseModel(Model):
    class Meta:
        database = Database.get_db()


class Settings(BaseModel):
    id = PrimaryKeyField(primary_key=True)

    # channel for check stat
    channel_name = CharField(null=False)

    # stat will send here
    print_to = CharField(null=False)

    # admin id for logs
    admin_to = CharField(null=False)

    # min number of subs (>0) for trigger send stat
    trigger_min_sub = IntegerField(null=False)

    # min number of unsubs (<0) for trigger send stat
    trigger_min_unsub = IntegerField(null=False)

    # min number of flow-users for trigger send stat
    trigger_min_flow = IntegerField(null=False)

    # trigger when users % every_odd == 0 (aka 'get 9000')
    trigger_every_odd = IntegerField(null=False, default=100)

    # trigger when new day occur
    trigger_new_day = BooleanField(null=False, default=True)

    # total users
    stat_total_users = IntegerField(null=False, default=0)

    # users from previous write
    stat_period_users = IntegerField(null=False, default=0)

    # day users
    stat_day_users = IntegerField(null=False, default=0)

    # delta users
    stat_delta_users = IntegerField(null=False, default=0)

    # max users
    stat_max_users = IntegerField(null=False, default=0)

    # last check time
    stat_last_check_time = DateTimeField(null=False, default=datetime.now(timezone(Config.TIMEZONE)))

    # no more 1 message more than ban_minutes
    write_ban_minutes = IntegerField(null=False, default=1)

    # last write time
    write_last_time = DateTimeField(null=False, default=datetime.now(timezone(Config.TIMEZONE)))

from peewee import SqliteDatabase

from config import Config


class Database:
    db = None

    @staticmethod
    def get_db():
        if Database.db is None:
            Database.db = SqliteDatabase(Config.SQLITE_DB_FULL_PATH)

        return Database.db

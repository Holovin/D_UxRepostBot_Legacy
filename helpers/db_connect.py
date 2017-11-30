from peewee import SqliteDatabase


class Database:
    db = None

    @staticmethod
    def get_db():
        if Database.db is None:
            Database.db = SqliteDatabase('settings.db')

        return Database.db

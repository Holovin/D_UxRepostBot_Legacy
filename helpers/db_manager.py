from helpers import db_models


class Serve:
    @staticmethod
    def create_tables(db):
        db.connect()
        db.create_tables([db_models.Settings])

    @staticmethod
    def drop_tables(db):
        db.connect()
        db.drop_tables([db_models.Settings])

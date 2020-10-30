from peewee import *
import datetime

DATABASE = "./database.sql"

db = SqliteDatabase(DATABASE)


class Rules(Model):
    created = DateTimeField(default=datetime.datetime.now)
    rule_text = TextField()
    user = CharField()

    class Meta:
        database = db


from peewee import *


DB = SqliteDatabase("./main.db")


class User(Model):
    userid = BigIntegerField()
    chatid = BigIntegerField()
    karma = IntegerField(default=0)

    class Meta:
        database = DB


def get_user(userid, chatid):
    user, _ = User.get_or_create(userid=userid, chatid=chatid)

    return user

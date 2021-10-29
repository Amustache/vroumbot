from peewee import *


DB = SqliteDatabase("./main.db")


class User(Model):
    userid = BigIntegerField()
    userfirstname = CharField(null=True)
    chatid = BigIntegerField()
    karma = IntegerField(default=0)

    class Meta:
        database = DB


def get_user(userid, chatid):
    user, _ = User.get_or_create(userid=userid, chatid=chatid)

    return user


def get_karma(chatid):
    users = User.select().where(User.chatid == chatid).order_by(User.karma.desc())

    return {user.userid: [user.userfirstname, user.karma] for user in users}

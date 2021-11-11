from peewee import *
from trello import TrelloClient

from secret import TRELLO_API_KEY, TRELLO_API_SECRET, TRELLO_FEEDBACK_BOARD, TRELLO_FEEDBACK_LIST

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


# Borrowed from https://github.com/django/django/blob/main/django/contrib/humanize/templatetags/humanize.py#L169, but worse
def naturaltime(delta):
    time_strings = {
        "now": "now",
        "second": ("in a second", "in {} seconds"),
        "minute": ("in a minute", "in {} minutes"),
        "hour": ("in an hour", "in {} hours"),
        "day": ("in a day", "in {} days"),
        "week": ("in a week", "in {} weeks"),
        "month": ("in a month", "in {} months"),
        "year": ("in a year", "in {} years"),
    }

    if delta.days != 0:
        if delta.days < 7:
            if delta.days == 1:
                return time_strings["day"][0]
            else:
                return time_strings["day"][1].format(delta.days)
        elif delta.days // 7 < 4:
            if delta.days // 7 == 1:
                return time_strings["week"][0]
            else:
                return time_strings["week"][1].format(delta.days // 7)
        elif delta.days // 7 // 4 < 12:
            if delta.days // 7 // 4 == 1:
                return time_strings["month"][0]
            else:
                return time_strings["month"][1].format(delta.days // 7 // 4)
        else:
            if delta.days // 7 // 4 // 12 == 1:
                return time_strings["year"][0]
            else:
                return time_strings["year"][1].format(delta.days // 7 // 4 // 12)
    else:
        if delta.seconds == 0:
            return time_strings["now"]
        elif delta.seconds < 60:
            if delta.seconds == 1:
                return time_strings["second"][0]
            else:
                return time_strings["second"][1].format(delta.seconds)
        elif delta.seconds // 60 < 60:
            if delta.seconds // 60 == 1:
                return time_strings["minute"][0]
            else:
                return time_strings["minute"][1].format(delta.seconds // 60)
        elif delta.seconds // 60 // 60 < 24:
            if delta.seconds // 60 // 60 == 1:
                return time_strings["hour"][0]
            else:
                return time_strings["hour"][1].format(delta.seconds // 60 // 60)


def add_feedback_to_trello(feedback):
    client = TrelloClient(
        api_key=TRELLO_API_KEY,
        api_secret=TRELLO_API_SECRET,
    )

    try:
        for board in client.list_boards():
            if board.name == TRELLO_FEEDBACK_BOARD:
                break

        if not board:
            print("Trello is not configured properly: board not found.")
            return

        for liste in board.list_lists():
            if liste.name == TRELLO_FEEDBACK_LIST:
                break

        if not liste:
            print("Trello is not configured properly: list not found.")
            return
    except:
        print("Trello is not configured properly: invalid credentials.")

    content, description = feedback

    liste.add_card(content, desc=description)

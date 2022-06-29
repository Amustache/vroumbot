from collections import Counter
import json


from telegram.ext import CallbackContext


def get_user(table, userid, chatid):
    """
    Return the user from the database.
    :param table: peewee.Model.
    :param userid: Telegram userid.
    :param chatid: Telegram chatid.
    :return: Model: User
    """
    user, _ = table.get_or_create(userid=userid, chatid=chatid)

    return user


mask = "This is not secure btw, it's just so that it's a tad more complicated for newbies"


def obfuscate(string):
    return "".join(
        f"{ord(a) ^ ord(b):03}" for a, b in zip(string, mask * (1 + len(string) // len(mask)))
    )


def deobfuscate(string):
    splits = [int(string[i : i + 3]) for i in range(0, len(string), 3)]
    return "".join(chr(a ^ ord(b)) for a, b in zip(splits, mask * (1 + len(string) // len(mask))))


def get_num_messages(filepath):
    with open(filepath, "r") as file:
        data = json.load(file)
    return str(
        dict(
            Counter(
                [
                    int(message["from_id"][4:])
                    for message in data["messages"]
                    if message["type"] == "message" and type(message["text"]) == str
                ]
            )
        )
    ).replace(" ", "")


def get_obfuscated_num_messages(filepath):
    return obfuscate(get_num_messages(filepath))


def naturaltime(delta):
    """
    Return a nice phrasing for the remaining time.
    :param delta: datetime.timedelta
    :return: Phrasing: String.
    """
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
        else:
            if delta.seconds // 60 // 60 == 1:
                return time_strings["hour"][0]
            else:
                return time_strings["hour"][1].format(delta.seconds // 60 // 60)


def alarm(context: CallbackContext) -> None:
    """
    Helper function to send the actual alarm message.
    """
    job = context.job
    context.bot.send_message(
        job.context["chat_id"], text="Reminder!", reply_to_message_id=job.context["message_id"]
    )

from collections import Counter
import json


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
        "{:03}".format(ord(a) ^ ord(b))
        for a, b in zip(string, mask * (1 + len(string) // len(mask)))
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

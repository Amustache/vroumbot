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

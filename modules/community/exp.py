import os
import random


from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler


from ..base import Base
from .helpers import get_user


def needed_exp(level, karma):
    if level == 0:
        return 0
    # Dirty hack
    if level == 1:
        return 5
    return int((level ** 3.14) * (1 - (karma / (level ** 3.14))))


class Exp(Base):
    def __init__(self, logger=None, table=None):
        commandhandlers = [MessageHandler(~Filters.command, self.add_message)]
        super().__init__(logger, commandhandlers, table, mediafolder="./media/levelup")

    def add_message(self, update: Update, context: CallbackContext):
        user = update.effective_user
        dbuser = get_user(self.table, user.id, update.message.chat.id)
        dbuser.num_messages += 1

        change = dbuser.level
        while dbuser.num_messages > needed_exp(dbuser.level, dbuser.karma):
            dbuser.level += 1

        if change != dbuser.level:
            filename = os.path.join(self._media(), random.choice(os.listdir(self._media())))
            with open(filename, "rb") as file:
                update.message.reply_document(
                    document=file,
                    caption="LEVEL UP!\n{} -> {}\n{} messages for {} karma.".format(
                        change, dbuser.level, dbuser.num_messages, dbuser.karma
                    ),
                )

        dbuser.save()

    def get_level(self, update: Update, context: CallbackContext):
        user = update.effective_user
        dbuser = get_user(self.table, user.id, update.message.chat.id)

        update.message.reply_text(
            "LEVEL {} ({} messages)".format(dbuser.level, dbuser.num_messages)
        )


# TODO
# state (start or stop)(if admin?)
# reset/import chat (with or without file)

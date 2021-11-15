#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

import logging


from peewee import BigIntegerField, CharField, IntegerField, Model, SqliteDatabase
from telegram.ext import Updater


from modules.bot import Bot
from modules.karma import Karma
from modules.remindme import RemindMe
from modules.special import Special
from secret import TOKEN


# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)

# Database
main_db = SqliteDatabase("./databases/main.db")


class User(Model):
    userid = BigIntegerField()
    userfirstname = CharField(null=True)
    chatid = BigIntegerField()
    karma = IntegerField(default=0)

    class Meta:
        database = main_db


main_db.connect()
main_db.create_tables([User])


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it the bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Commands
    Bot(logger).add_commands(dispatcher)
    Special(logger).add_commands(dispatcher)
    Karma(logger, table=User).add_commands(dispatcher)
    RemindMe(logger).add_commands(dispatcher)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()

#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from collections import defaultdict
from peewee import *
from secret import TOKEN

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


db = SqliteDatabase("./main.db")

class User(Model):
    userid = BigIntegerField()
    chatid = BigIntegerField()
    karma = IntegerField(default=0)

    class Meta:
        database = db


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Bonjour {user.mention_markdown_v2()} \!',
        reply_markup=ForceReply(selective=True),
    )


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def vroum(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Vroum!')


def vroom(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('😠')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def plus(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user

        if user == update.effective_user:
            update.message.reply_text("Humble bragging, amarite?")
            return

        dbuser = get_user(user.id, update.message.chat.id)
        dbuser.karma += 1
        dbuser.save()

        update.message.reply_text("+1 for {} ({} points).".format(user.first_name, dbuser.karma))


def moins(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user

        if user == update.effective_user:
            update.message.reply_text("Don't be so harsh on yourself.")
            return

        dbuser = get_user(user.id, update.message.chat.id)
        dbuser.karma -= 1
        dbuser.save()

        update.message.reply_text("-1 for {} ({} points).".format(user.first_name, dbuser.karma))


def getkarma(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    else:
        user = update.effective_user

    karma = get_user(user.id, update.message.chat.id).karma
    update.message.reply_text("{} has {} points.".format(user.first_name, karma))


def userid(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        update.message.reply_text(user.id)
    else:
        user = update.effective_user
        update.message.reply_text(user.id)


def get_user(userid, chatid):
    user = User.get_or_create(userid=userid, chatid=chatid)

    return user


def main() -> None:
    db.connect()
    db.create_tables([User])

    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(TOKEN)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("hello", start))
    dispatcher.add_handler(CommandHandler("hi", start))
    dispatcher.add_handler(CommandHandler("bonjour", start))
    dispatcher.add_handler(CommandHandler("vroum", vroum))
    dispatcher.add_handler(CommandHandler("vroom", vroom))
    dispatcher.add_handler(CommandHandler("plus", plus))
    dispatcher.add_handler(CommandHandler("pos", plus))
    dispatcher.add_handler(CommandHandler("moins", moins))
    dispatcher.add_handler(CommandHandler("minus", moins))
    dispatcher.add_handler(CommandHandler("min", moins))
    dispatcher.add_handler(CommandHandler("neg", moins))
    dispatcher.add_handler(CommandHandler("userid", userid))
    dispatcher.add_handler(CommandHandler("id", userid))
    dispatcher.add_handler(CommandHandler("getkarma", getkarma))
    dispatcher.add_handler(CommandHandler("karma", getkarma))
    # dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

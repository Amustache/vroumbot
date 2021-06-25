#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.
import logging
import os
import random


from telegram import ForceReply, Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater


from helpers import DB, get_user, User
from secret import ADMIN_ID, TOKEN


# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr"Bonjour {user.mention_markdown_v2()} \!",
        reply_markup=ForceReply(selective=True),
    )

    logger.info("%s says hi!", user.first_name)


def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Help!")

    logger.info("%s needs help!", update.effective_user.first_name)


def vroum(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Vroum!")

    logger.info("%s gets a Vroum!", update.effective_user.first_name)


def vroom(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("😠")

    logger.info("%s gets a 😠!", update.effective_user.first_name)


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

    logger.info("%s want an echo!", update.effective_user.first_name)


def plus(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user

        if user == update.effective_user:
            update.message.reply_text("Humble bragging, amarite?")

            logger.info("%s wants to pos themselves!", user.first_name)
            return

        dbuser = get_user(user.id, update.message.chat.id)
        dbuser.karma += 1
        dbuser.save()

        update.message.reply_to_message.reply_text("+1 for {} ({} points).".format(user.first_name, dbuser.karma))

        logger.info("%s gets a +1!", user.first_name)


def moins(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user

        if user == update.effective_user:
            update.message.reply_text("Don't be so harsh on yourself.")

            logger.info("%s wants to neg themselves!", user.first_name)
            return

        dbuser = get_user(user.id, update.message.chat.id)
        dbuser.karma -= 1
        dbuser.save()

        update.message.reply_to_message.reply_text("-1 for {} ({} points).".format(user.first_name, dbuser.karma))

        logger.info("%s gets a -1!", user.first_name)


def getkarma(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    else:
        user = update.effective_user

    karma = get_user(user.id, update.message.chat.id).karma
    update.message.reply_text("{} has {} points.".format(user.first_name, karma))

    logger.info("%s has %d karma!", user.first_name, karma)


def userid(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        update.message.reply_text(user.id)
    else:
        user = update.effective_user
        update.message.reply_text(user.id)

    logger.info("%s wants their ID! It is %d.", user.first_name, user.id)


def chatid(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.chat.id)

    logger.info("%s wants the chat ID! It is %d.", update.effective_user.first_name, update.message.chat.id)


def random_cat(update: Update, context: CallbackContext) -> None:
    folder = "./cats"
    filename = os.path.join(folder, random.choice(os.listdir(folder)))
    meow = random.choice(
        [
            "meo",
            "meong",
            "meow",
            "mèu",
            "miaau",
            "miaou",
            "miau",
            "miauw",
            "喵",
            "喵",
            "喵",
            "miao",
            "miaow",
            "miyav",
            "miav",
            "mjau",
            "միյաւ",
            "ম্যাঁও",
            "meogre",
            "miaŭ",
            "ngiyaw",
            "میاؤں",
            "mjá",
            "mňau",
            "ngeung",
            "კნავილი",
            "njäu",
            "ņau",
            "nyav",
            "mi'au",
            "νιάου",
            "にゃー",
            "야옹",
            "냥",
            "מיאו",
            "מיאַו",
            "мјау",
            "miáú",
            "miau",
            "nyaú",
            "мяу",
            "ngiau",
            "mijav",
            "mia'wj",
            "میو",
            "مُواء",
        ]
    )
    update.message.reply_photo(photo=open(filename, "rb"), caption=meow)

    logger.info("%s wants a cat pic!", update.effective_user.first_name)


def brrou(update: Update, context: CallbackContext) -> None:
    folder = "./brrou"
    filename = os.path.join(folder, random.choice(os.listdir(folder)))
    meow = random.choice(["brrou", "Brrou", "b r r o u", "BROU", "B R R O U", "tut"])
    update.message.reply_photo(photo=open(filename, "rb"), caption=meow)

    logger.info("%s wants a Brrou pic!", update.effective_user.first_name)


def boop(update: Update, context: CallbackContext) -> None:
    if "/beep" in update.message.text:
        text = "boop"
    elif "/boop" in update.message.text:
        text = "beep"
    else:
        text = "..."

    update.message.reply_text(text)

    logger.info("%s gets a %s!", update.effective_user.first_name, text)


def tut(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("tut")

    logger.info("%s gets a tut!", update.effective_user.first_name)


def toutoutoutou(update: Update, context: CallbackContext) -> None:
    update.message.reply_sticker("CAACAgIAAxkBAAECenJg1f163I_8Uzc9UjymlOLV9yyxWAACywADwPsIAAEtUj0YdWOU7iAE")

    logger.info("%s gets a toutoutoutou!", update.effective_user.first_name)


def feedback(update: Update, context: CallbackContext) -> None:
    user = update.effective_user.first_name
    _, message = update.message.text.split(" ", 1)
    message = '{} says "{}"'.format(user, message)
    context.bot.sendMessage(chat_id=ADMIN_ID, text=message)

    logger.info("%s", message)


def main() -> None:
    DB.connect()
    DB.create_tables([User])

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
    dispatcher.add_handler(CommandHandler("chatid", chatid))
    dispatcher.add_handler(CommandHandler("here", chatid))

    dispatcher.add_handler(CommandHandler("getkarma", getkarma))
    dispatcher.add_handler(CommandHandler("karma", getkarma))

    dispatcher.add_handler(CommandHandler("cat", random_cat))
    dispatcher.add_handler(CommandHandler("chat", random_cat))
    dispatcher.add_handler(CommandHandler("kot", random_cat))

    dispatcher.add_handler(CommandHandler("brrou", brrou))

    dispatcher.add_handler(CommandHandler("tut", tut))

    dispatcher.add_handler(CommandHandler("boop", boop))
    dispatcher.add_handler(CommandHandler("beep", boop))

    dispatcher.add_handler(CommandHandler("feedback", feedback))
    dispatcher.add_handler(CommandHandler("suggestion", feedback))
    dispatcher.add_handler(CommandHandler("suggest", feedback))

    dispatcher.add_handler(CommandHandler("toutoutoutou", toutoutoutou))
    # dispatcher.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    # dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()

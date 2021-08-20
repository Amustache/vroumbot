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
    """
    Don't forget to update this manually.
    """

    text = """Available commands:
- start, hello, hi => start;
- bonjour => bonjour;
- stupid => stupid;
- trolled => trolled;
- vroum => vroum;
- vroom => vroom;
- plus, pos, bravo => plus;
- moins, minus, min, neg, non => moins;
- userid, id => userid;
- chatid, here => chatid;
- karma, getkarma => getkarma;
- cat, chat, kot => random_cat;
- brrou => brrou;
- froj => froj;
- tut => tut;
- beep, boop => boop;
- feedback, suggestion, suggest => feedback;
- toutoutoutoum4a => toutoutoutoum4a;
- toutoutoutou => toutoutoutou;
- all_commands => help_command;"""
    update.message.reply_text(text)

    logger.info("%s wants to see all commands!", update.effective_user.first_name)


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


def froj(update: Update, context: CallbackContext) -> None:
    folder = "./froj"
    filename = os.path.join(folder, random.choice(os.listdir(folder)))
    meow = "https://frogdetective.net/"
    update.message.reply_photo(photo=open(filename, "rb"), caption=meow)

    logger.info("%s wants a froj pic!", update.effective_user.first_name)


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


def toutoutoutoum4a(update: Update, context: CallbackContext) -> None:
    update.message.reply_audio(audio=open("./media/toutoutoutou.m4a", "rb")).reply_sticker(
        "CAACAgIAAxkBAAECenJg1f163I_8Uzc9UjymlOLV9yyxWAACywADwPsIAAEtUj0YdWOU7iAE"
    )

    logger.info("%s gets a toutoutoutou!", update.effective_user.first_name)


def bonjour(update: Update, context: CallbackContext) -> None:
    update.message.reply_video(video=open("./media/setup.mp4", "rb"))

    logger.info("%s gets a bonjour à toutes et tous!", update.effective_user.first_name)


def stupid(update: Update, context: CallbackContext) -> None:
    update.message.reply_video(video=open("./media/stupid.mp4", "rb"))

    logger.info("%s is being really stupid right now!", update.effective_user.first_name)


def keysmash(update: Update, context: CallbackContext) -> None:
    letters_normal = ["j", "h", "l", "r", "d", "s", "m", "J", "f", "k", "g"]
    letters_frustration = ["l", "h", "r", "m", "g"]

    letters = letters_frustration if random.randint(1, 9) == 1 else letters_normal

    mu = 12.777777777778
    sigma = 2.1998877636915
    length = int(random.gauss(mu, sigma))
    result = oldletter = newletter = random.choice(letters)

    for i in range(length):
        while oldletter == newletter:
            newletter = random.choice(letters)
        result += newletter
        oldletter = newletter

    update.message.reply_text(result)


def oh(update: Update, context: CallbackContext) -> None:
    mu = 3
    sigma = 2
    length = -1
    while length < 1:
        length = int(random.gauss(mu, sigma))

    result = "o" * length + "h"
    result = [l.upper() if random.randint(1, 6) == 1 else l for l in result]

    update.message.reply_text(result)


def xd(update: Update, context: CallbackContext) -> None:
    mu = 3
    sigma = 2
    length = -1
    while length < 1:
        length = int(random.gauss(mu, sigma))

    if random.randint(1, 2) == 1:
        result = "X" + "D" * length
    else:
        result = "a" + "y" * length

    update.message.reply_text(result)


def trolled(update: Update, context: CallbackContext) -> None:
    update.message.reply_video(video=open("./media/troll.mp4", "rb"))

    logger.info("%s's just been trolled!", update.effective_user.first_name)


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
    dispatcher.add_handler(CommandHandler(["start", "hello", "hi"], start))

    dispatcher.add_handler(CommandHandler("bonjour", bonjour))
    dispatcher.add_handler(CommandHandler("stupid", stupid))
    dispatcher.add_handler(CommandHandler("trolled", trolled))

    dispatcher.add_handler(CommandHandler("vroum", vroum))
    dispatcher.add_handler(CommandHandler("vroom", vroom))

    dispatcher.add_handler(CommandHandler(["plus", "pos", "bravo"], plus))
    dispatcher.add_handler(CommandHandler(["moins", "minus", "min", "neg", "non"], moins))

    dispatcher.add_handler(CommandHandler(["userid", "id"], userid))
    dispatcher.add_handler(CommandHandler(["chatid", "here"], chatid))

    dispatcher.add_handler(CommandHandler(["karma", "getkarma"], getkarma))

    dispatcher.add_handler(CommandHandler(["cat", "chat", "kot"], random_cat))

    dispatcher.add_handler(CommandHandler("brrou", brrou))

    dispatcher.add_handler(CommandHandler("froj", froj))

    dispatcher.add_handler(CommandHandler("tut", tut))

    dispatcher.add_handler(CommandHandler(["beep", "boop"], boop))

    dispatcher.add_handler(CommandHandler(["feedback", "suggestion", "suggest"], feedback))

    dispatcher.add_handler(CommandHandler("toutoutoutoum4a", toutoutoutoum4a))
    dispatcher.add_handler(CommandHandler("toutoutoutou", toutoutoutou))

    dispatcher.add_handler(CommandHandler(["keysmash", "bottom"], keysmash))
    dispatcher.add_handler(CommandHandler(["oh", "ooh", "oooh"], oh))
    dispatcher.add_handler(CommandHandler(["ay", "ayy", "ayyy", "xd", "xdd", "xddd"], xd))

    dispatcher.add_handler(CommandHandler("all_commands", help_command))

    commands = ""
    for handler in dispatcher.handlers[0]:
        commands += "- {} => {};\n".format(", ".join(handler.command), handler.callback.__name__)
    print("Available commands:\n{}".format(commands))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()

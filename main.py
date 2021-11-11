#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.
import datetime
import logging
import os
import random


from bs4 import BeautifulSoup
from PIL import Image
from telegram import constants, ForceReply, Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, Filters, MessageHandler, Updater
import dateparser
import requests


from helpers import DB, get_karma, get_user, naturaltime, User
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

    logger.info("{} says hi!".format(user.first_name))


def help_command(update: Update, context: CallbackContext) -> None:
    """
    Don't forget to update this manually.
    """

    text = """Available commands:
- start, hello, hi => start;
- bonjour => bonjour;
- stupid => stupid;
- trolled => trolled;
- heretic => heretic;
- bricole => bricole;
- vroum => vroum;
- vroom => vroom;
- plus, pos, bravo => plus;
- moins, minus, min, neg, non => moins;
- userid, id => userid;
- chatid, here => chatid;
- messageid, this, that => messageid;
- karma, getkarma => getkarma;
- cat, chat, kot => random_cat;
- brrou => brrou;
- froj => froj;
- tut => tut;
- beep, boop => boop;
- feedback, suggestion, suggest => feedback;
- toutoutoutoum4a => toutoutoutoum4a;
- toutoutoutou => toutoutoutou;
- spin, speen => spin;
- keysmash, bottom => keysmash;
- oh, ooh, oooh => oh;
- ay, ayy, ayyy, xd, xdd, xddd => xd;
- genre, gender, sexe, sex, sexx, genr => gender;
- whois, whoissciper, sciper => whoissciper;
- whoisnsfw, whoisscipernsfw, scipernsfw => whoisscipernsfw;
- help, all_commands => help_command;"""
    update.message.reply_text(text)

    logger.info("{} wants to see all commands!".format(update.effective_user.first_name))


def contribute(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Want to contribute? Use `/feedback <your proposition>` or go to https://github.com/Amustache/vroumbot!")

    logger.info("{} wants to contribute!".format(update.effective_user.first_name))


def vroum(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Vroum!")

    logger.info("{} gets a Vroum!".format(update.effective_user.first_name))


def vroom(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("😠")

    logger.info("{} gets a 😠!".format(update.effective_user.first_name))


def echo(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.text)

    logger.info("{} want an echo!".format(update.effective_user.first_name))


def plus(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        dbuser = get_user(user.id, update.message.chat.id)

        if user == update.effective_user:
            update.message.reply_text("Humble bragging, amarite?")
            logger.info("{} wants to pos themselves!".format(user.first_name))

        else:
            dbuser.karma += 1
            update.message.reply_to_message.reply_text("+1 for {} ({} points).".format(user.first_name, dbuser.karma))
            logger.info("{} gets a +1!".format(user.first_name))

        dbuser.userfirstname = user.first_name
        dbuser.save()
    else:
        update.message.reply_text("You must respond to a message to give karma.")


def moins(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        dbuser = get_user(user.id, update.message.chat.id)

        if user == update.effective_user:
            update.message.reply_text("Don't be so harsh on yourself.")
            logger.info("{} wants to neg themselves!".format(user.first_name))

        else:
            dbuser.karma -= 1
            update.message.reply_to_message.reply_text("-1 for {} ({} points).".format(user.first_name, dbuser.karma))
            logger.info("{} gets a -1!".format(user.first_name))

        dbuser.userfirstname = user.first_name
        dbuser.save()
    else:
        update.message.reply_text("You must respond to a message to give karma.")


def getkarma(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        dbuser = get_user(user.id, update.message.chat.id)
        dbuser.userfirstname = user.first_name
        dbuser.save()

        update.message.reply_text("{} has {} points.".format(dbuser.userfirstname, dbuser.karma))
        logger.info("{} has {} karma!".format(dbuser.userfirstname, dbuser.karma))

    else:
        karmas = get_karma(update.message.chat.id)

        all = []
        for id, data in karmas.items():
            username, karma = data
            if not username:
                username = "<please trigger karma action for name>"
            if karma != 0:
                all.append("- {}: {} points.".format(username, karma))

        update.message.reply_text("\n".join(all))
        logger.info("{} wants to know the karmas!".format(update.effective_user.first_name))


def dad(update: Update, context: CallbackContext) -> None:
    endpoint = "http://dadjokes.online/noecho"
    resp = requests.get(url=endpoint)
    try:
        data = resp.json()
        opener, punchline, _ = data["Joke"].values()
    except:
        update.message.reply_text("No more dad jokes )':.")
        return

    update.message.reply_text(opener).reply_text(punchline)


def userid(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
        update.message.reply_text(user.id)
    else:
        user = update.effective_user
        update.message.reply_text(user.id)

    logger.info("{} wants their ID! It is {}.".format(user.first_name, user.id))


def chatid(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(update.message.chat.id)

    logger.info("{} wants the chat ID! It is {}.".format(update.effective_user.first_name, update.message.chat.id))


def messageid(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        update.message.reply_text("{} in {}".format(update.message.reply_to_message.message_id, update.message.chat.id))

        logger.info(
            "{} wants the message ID! It is {} in {}.".format(update.effective_user.first_name, update.message.message_id, update.message.chat.id)
        )


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

    logger.info("{} wants a cat pic!".format(update.effective_user.first_name))


def brrou(update: Update, context: CallbackContext) -> None:
    folder = "./brrou"
    filename = os.path.join(folder, random.choice(os.listdir(folder)))
    meow = random.choice(["brrou", "Brrou", "b r r o u", "BROU", "B R R O U", "tut"])
    update.message.reply_photo(photo=open(filename, "rb"), caption=meow)

    logger.info("{} wants a Brrou pic!".format(update.effective_user.first_name))


def froj(update: Update, context: CallbackContext) -> None:
    folder = "./froj"
    filename = os.path.join(folder, random.choice(os.listdir(folder)))
    meow = "https://frogdetective.net/"
    update.message.reply_photo(photo=open(filename, "rb"), caption=meow)

    logger.info("{} wants a froj pic!".format(update.effective_user.first_name))


def boop(update: Update, context: CallbackContext) -> None:
    if "/beep" in update.message.text:
        text = "boop"
    elif "/boop" in update.message.text:
        text = "beep"
    else:
        text = "..."

    update.message.reply_text(text)

    logger.info("{} gets a {}!".format(update.effective_user.first_name, text))


def tut(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("tut")

    logger.info("{} gets a tut!".format(update.effective_user.first_name))


def spin(update: Update, context: CallbackContext) -> None:
    update.message.reply_audio(audio=open("./media/spin.mp3", "rb"))

    logger.info("{} gets a SPEEN!".format(update.effective_user.first_name))


def toutoutoutou(update: Update, context: CallbackContext) -> None:
    update.message.reply_sticker("CAACAgIAAxkBAAECenJg1f163I_8Uzc9UjymlOLV9yyxWAACywADwPsIAAEtUj0YdWOU7iAE")

    logger.info("{} gets a toutoutoutou!".format(update.effective_user.first_name))


def toutoutoutoum4a(update: Update, context: CallbackContext) -> None:
    update.message.reply_audio(audio=open("./media/toutoutoutou.m4a", "rb")).reply_sticker(
        "CAACAgIAAxkBAAECenJg1f163I_8Uzc9UjymlOLV9yyxWAACywADwPsIAAEtUj0YdWOU7iAE"
    )

    logger.info("{} gets a toutoutoutou!".format(update.effective_user.first_name))


def bonjour(update: Update, context: CallbackContext) -> None:
    update.message.reply_video(video=open("./media/setup.mp4", "rb"))

    logger.info("{} gets a bonjour à toutes et tous!".format(update.effective_user.first_name))


def stupid(update: Update, context: CallbackContext) -> None:
    update.message.reply_video(video=open("./media/stupid.mp4", "rb"))

    logger.info("{} is being really stupid right now!".format(update.effective_user.first_name))


def heretic(update: Update, context: CallbackContext) -> None:
    update.message.reply_video(video=open("./media/heretic.mp4", "rb"))

    logger.info("{} likes being a heretic!".format(update.effective_user.first_name))


def bricole(update: Update, context: CallbackContext) -> None:
    update.message.reply_video(video=open("./media/bricole.mp4", "rb"))

    logger.info("{} wants to BRICOLE!".format(update.effective_user.first_name))


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

    logger.info("{} is keysmashing!".format(update.effective_user.first_name))


def oh(update: Update, context: CallbackContext) -> None:
    mu = 3
    sigma = 2
    length = -1
    while length < 1:
        length = int(random.gauss(mu, sigma))

    result = "o" * length + "h"
    result = "".join([l.upper() if random.randint(1, 6) == 1 else l for l in result])

    update.message.reply_text(result)

    logger.info("{} is in awe!".format(update.effective_user.first_name))


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

    logger.info("{} is in XDing real hard!".format(update.effective_user.first_name))


def trolled(update: Update, context: CallbackContext) -> None:
    update.message.reply_video(video=open("./media/troll.mp4", "rb"))

    logger.info("{}'s just been trolled!".format(update.effective_user.first_name))


def gender(update: Update, context: CallbackContext) -> None:
    context.bot.forward_message(update.message.chat.id, "59804991", "2626")
    context.bot.forward_message(update.message.chat.id, "59804991", "2627")

    logger.info("{} got gendered!".format(update.effective_user.first_name))


def feedback(update: Update, context: CallbackContext) -> None:
    user = update.effective_user.first_name
    _, message = update.message.text.split(" ", 1)
    message = '{} says "{}"'.format(user, message)
    context.bot.sendMessage(chat_id=ADMIN_ID, text=message)

    logger.info("{}".format(message))


def carpe(update: Update, context: CallbackContext) -> None:
    if update.effective_user.username == "ReallyCrazyMan" and random.randint(1, 6) == 6:
        update.message.reply_photo(photo=open("./media/opinion.jpg", "rb"))


def whoissciper(update: Update, context: CallbackContext) -> None:
    _, sciper = update.message.text.split(" ", 1)
    try:
        sciper = int(sciper)
        if sciper < 100000 or sciper > 999999:
            raise Exception  # epic coding
    except:
        update.message.reply_text("Not a valid SCIPER.")
        return

    URL = "https://people.epfl.ch/{}".format(sciper)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    try:
        name = soup.find_all("h1", class_="mr-3")[0].text
    except:
        update.message.reply_text("SCIPER not found or not public.")
        return

    update.message.reply_text("{} is {}.".format(sciper, name))


def whoisscipernsfw(update: Update, context: CallbackContext) -> None:
    _, sciper = update.message.text.split(" ", 1)
    try:
        sciper = int(sciper)
        if sciper < 100000 or sciper > 999999:
            raise Exception  # epic coding
    except:
        update.message.reply_text("Not a valid SCIPER b-baka.")
        return

    URL = "https://nhentai.to/g/{}".format(sciper)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")

    if soup.title.text == "Not Found":
        update.message.reply_text("{} seems to be pure and innocent...".format(sciper))
        return

    tags = [thing for thing in soup.findAll("div", {"class": "tag-container"}) if "Tags" in thing.text]
    if tags:
        tags_text = []
        for tag in [tag.text.strip() for tag in tags[0].findAll("a", {"class": "tag"})]:
            tags_text.append(tag)
        if tags_text:
            update.message.reply_text("{} is linked to {}.".format(sciper, ", ".join(tags_text)))
            return

    update.message.reply_text("{} is a secretive pervert.".format(sciper))


def nft(update: Update, context: CallbackContext) -> None:
    if update.message.reply_to_message:
        user = update.message.reply_to_message.from_user
    else:
        user = update.effective_user

    userid = user.id

    filename = "./nft/{}.png".format(userid)

    if not os.path.isfile(filename):
        binuserid = bin(userid)[2:].zfill(64)

        vroumbot = "vroumbot"
        binvroumbot = "".join(format(ord(x), "b").zfill(8) for x in vroumbot)

        img = Image.new("RGBA", (64, 64), "black")
        pixels = img.load()

        def magic(i, j, userid):
            ij = i * j
            iju = i * j * userid
            pix1 = hash(vroumbot[iju % len(vroumbot)] + str(iju)) % 256
            pix2 = hash(vroumbot[iju % len(vroumbot)] + str(ij)) % 256
            pix3 = hash(vroumbot[ij % len(vroumbot)] + str(iju)) % 256
            transp = 255

            if pix1 == pix2 == pix3:
                transp = 0

            return (pix1, pix2, pix3, transp)

        for i in range(img.size[0]):
            for j in range(img.size[1]):
                pixels[i, j] = magic(i, j, userid)

        for i, p in enumerate(binuserid):
            if p == "1":
                pixels[i, 0] = (0, 0, 0, 255)
            else:
                pixels[i, 0] = (0, 0, 0, 0)

        for j, p in enumerate(binvroumbot):
            if p == "1":
                pixels[0, j] = (0, 0, 0, 255)
            else:
                pixels[0, j] = (0, 0, 0, 0)

        img.resize((512, 512), Image.NEAREST).save(filename)

    update.message.reply_photo(
        photo=open(filename, "rb"), caption="This is {}'s exclusive NFT, do not use without permission!".format(user.first_name)
    )

    logger.info("{} now has an NFT!".format(user.first_name))


def alarm(context: CallbackContext) -> None:
    job = context.job
    context.bot.send_message(job.context["chat_id"], text="Reminder!", reply_to_message_id=job.context["message_id"])


def remindme(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    message_id = update.message.message_id

    try:
        _, message = update.message.text.split(" ", 1)
        interpreted = dateparser.parse(message)
        if not interpreted:
            update.message.reply_text("I didn't understand, sorry...")
            return

        delta = (interpreted - datetime.datetime.now()) + datetime.timedelta(seconds=1)
        if delta.total_seconds() < 0:
            if delta.total_seconds() < -1:
                update.message.reply_text("Sorry we can not go back to future!")
            else:
                update.message.reply_text("Okay, that may be a bit too close anyway.")
            return

        context.job_queue.run_once(
            alarm, delta.total_seconds(), context={"chat_id": chat_id, "message_id": message_id}, name="{}_{}".format(chat_id, message_id)
        )

        update.message.reply_text("I will remind you this {} ({})!".format(naturaltime(delta), str(delta).split(".")[0]))
    except (IndexError, ValueError):
        update.message.reply_text("It seems like you used that command wrong. (:.")


def allremindme(update: Update, context: CallbackContext) -> None:
    jobs = context.job_queue.jobs()
    if update.message.chat.type == constants.CHAT_SUPERGROUP:
        liste = [
            "- #<a href='https://t.me/c/{}/{}'>{}</a>: {}.".format(
                str(job.context["chat_id"])[4:], job.context["message_id"], job.context["message_id"], str(job.next_t).split(".")[0]
            )
            for job in jobs
            if job.context["chat_id"] == update.message.chat_id
        ]
    else:
        liste = [
            "- #{}: {}.".format(i, str(job.next_t).split(".")[0]) for i, job in enumerate(jobs) if job.context["chat_id"] == update.message.chat_id
        ]
    update.message.reply_text("List of reminders:\n{}".format("\n".join(liste)), parse_mode=constants.PARSEMODE_HTML)


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

    dispatcher.add_handler(CommandHandler(["contribute", "github", "source", "git", "contrib"], contribute))

    dispatcher.add_handler(CommandHandler("bonjour", bonjour))
    dispatcher.add_handler(CommandHandler("stupid", stupid))
    dispatcher.add_handler(CommandHandler("trolled", trolled))
    dispatcher.add_handler(CommandHandler("heretic", heretic))
    dispatcher.add_handler(CommandHandler("bricole", bricole))

    dispatcher.add_handler(CommandHandler("vroum", vroum))
    dispatcher.add_handler(CommandHandler("vroom", vroom))

    dispatcher.add_handler(CommandHandler(["plus", "pos", "bravo"], plus))
    dispatcher.add_handler(CommandHandler(["moins", "minus", "min", "neg", "non"], moins))

    dispatcher.add_handler(CommandHandler(["userid", "id"], userid))
    dispatcher.add_handler(CommandHandler(["chatid", "here"], chatid))
    dispatcher.add_handler(CommandHandler(["messageid", "this", "that"], messageid))

    dispatcher.add_handler(CommandHandler(["karma", "getkarma"], getkarma))

    dispatcher.add_handler(CommandHandler(["cat", "chat", "kot"], random_cat))

    dispatcher.add_handler(CommandHandler("brrou", brrou))

    dispatcher.add_handler(CommandHandler("froj", froj))

    dispatcher.add_handler(CommandHandler("tut", tut))

    dispatcher.add_handler(CommandHandler(["beep", "boop"], boop))

    dispatcher.add_handler(CommandHandler(["feedback", "suggestion", "suggest"], feedback))

    dispatcher.add_handler(CommandHandler("toutoutoutoum4a", toutoutoutoum4a))
    dispatcher.add_handler(CommandHandler("toutoutoutou", toutoutoutou))

    dispatcher.add_handler(CommandHandler(["spin", "speen"], spin))

    dispatcher.add_handler(CommandHandler(["keysmash", "bottom"], keysmash))
    dispatcher.add_handler(CommandHandler(["oh", "ooh", "oooh"], oh))
    dispatcher.add_handler(CommandHandler(["ay", "ayy", "ayyy", "xd", "xdd", "xddd"], xd))

    dispatcher.add_handler(CommandHandler(["genre", "gender", "sexe", "sex", "sexx", "genr"], gender))

    dispatcher.add_handler(MessageHandler(~Filters.command, carpe))

    dispatcher.add_handler(CommandHandler(["whois", "whoissciper", "sciper"], whoissciper))
    dispatcher.add_handler(CommandHandler(["whoisnsfw", "whoisscipernsfw", "scipernsfw"], whoisscipernsfw))

    dispatcher.add_handler(CommandHandler(["nft", "scam"], nft))

    dispatcher.add_handler(CommandHandler(["dad", "dadjoke"], dad))

    dispatcher.add_handler(CommandHandler(["remindme", "remind_me", "set", "alarm"], remindme))
    dispatcher.add_handler(
        CommandHandler(
            [
                "listremindme",
                "listjobs",
                "listalarms",
            ],
            allremindme,
        )
    )

    dispatcher.add_handler(CommandHandler(["help", "all_commands"], help_command))

    commands = ""
    for handler in dispatcher.handlers[0]:
        try:
            commands += "- {} => {};\n".format(", ".join(handler.command), handler.callback.__name__)
        except:
            continue
    print("Available commands:\n{}".format(commands))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()

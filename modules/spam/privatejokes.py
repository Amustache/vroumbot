import random


from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler
import requests


from ..base import Base


class PrivateJoke(Base):
    def __init__(self, logger=None):
        commandhandlers = [
            CommandHandler("toutoutoutou", self.toutoutoutou),
            CommandHandler("toutoutoutoum4a", self.toutoutoutoum4a),
            CommandHandler(["whois", "whoissciper", "sciper"], self.whoissciper),
            CommandHandler(["whoisnsfw", "whoisscipernsfw", "scipernsfw"], self.whoisscipernsfw),
            CommandHandler(["genre", "gender", "sexe", "sex", "sexx", "genr"], self.gender),
            MessageHandler(~Filters.command, self.carpe),
        ]
        super().__init__(logger, commandhandlers, mediafolder="./media")

    def toutoutoutou(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_sticker("CAACAgIAAxkBAAECenJg1f163I_8Uzc9UjymlOLV9yyxWAACywADwPsIAAEtUj0YdWOU7iAE")

        self.logger.info("{} gets a toutoutoutou!".format(update.effective_user.first_name))

    def toutoutoutoum4a(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_audio(audio=open(self._media("toutoutoutou.m4a"), "rb")).reply_sticker(
            "CAACAgIAAxkBAAECenJg1f163I_8Uzc9UjymlOLV9yyxWAACywADwPsIAAEtUj0YdWOU7iAE"
        )

        self.logger.info("{} gets a toutoutoutou!".format(update.effective_user.first_name))

    def whoissciper(self, update: Update, context: CallbackContext) -> None:
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

    def whoisscipernsfw(self, update: Update, context: CallbackContext) -> None:
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

    def gender(self, update: Update, context: CallbackContext) -> None:
        context.bot.forward_message(update.message.chat.id, "59804991", "2626")
        context.bot.forward_message(update.message.chat.id, "59804991", "2627")

        self.logger.info("{} got gendered!".format(update.effective_user.first_name))

    def carpe(self, update: Update, context: CallbackContext) -> None:
        if update.effective_user.username == "ReallyCrazyMan" and random.randint(1, 6) == 6:
            update.message.reply_photo(photo=open(self._media("opinion.jpg"), "rb"))

"""
Private jokes! Yay!
"""
import random


from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler
import requests


from ..base import Base


class PrivateJoke(Base):
    """
    Private jokes! Yay!
    """

    def __init__(self, logger=None):
        commandhandlers = [
            CommandHandler("toutoutoutou", self.toutoutoutou),
            CommandHandler("toutoutoutoum4a", self.toutoutoutoum4a),
            CommandHandler(["whois", "whoissciper", "sciper"], self.whoissciper),
            CommandHandler(["whoisnsfw", "whoisscipernsfw", "scipernsfw"], self.whoisscipernsfw),
            CommandHandler(["genre", "gender", "sexe", "sex", "sexx", "genr"], self.gender),
            MessageHandler(~Filters.command, self.carpe),
            CommandHandler(["saisine", "ccg"], self.saisine),
            CommandHandler(["horny"], self.horny),
            CommandHandler(["crypto", "bully"], self.crypto),
            CommandHandler(
                ["stopdoing", "stopdoingstopdoing", "stopdoingstopdoings"], self.stopdoing
            ),
        ]
        super().__init__(logger, commandhandlers, mediafolder="./media")

    def toutoutoutou(self, update: Update, context: CallbackContext) -> None:
        """
        The rythm is growing...
        """
        update.message.reply_sticker(
            "CAACAgIAAxkBAAECenJg1f163I_8Uzc9UjymlOLV9yyxWAACywADwPsIAAEtUj0YdWOU7iAE"
        )

        self.logger.info("{} gets a toutoutoutou!".format(update.effective_user.first_name))

    def toutoutoutoum4a(self, update: Update, context: CallbackContext) -> None:
        """
        Actual rythm growing.
        """
        with open(self._media("toutoutoutou.m4a"), "rb") as file:
            update.message.reply_audio(audio=file).reply_sticker(
                "CAACAgIAAxkBAAECenJg1f163I_8Uzc9UjymlOLV9yyxWAACywADwPsIAAEtUj0YdWOU7iAE"
            )

        self.logger.info("{} gets a toutoutoutou!".format(update.effective_user.first_name))

    def whoissciper(self, update: Update, context: CallbackContext) -> None:
        """
        SCIPER to name.
        """
        _, sciper = update.message.text.split(" ", 1)
        try:
            sciper = int(sciper)
            if sciper < 100000 or sciper > 999999:
                raise ValueError
        except ValueError:
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

        self.logger.info(
            "{} wants informations about a SCIPER!".format(update.effective_user.first_name)
        )

    def whoisscipernsfw(self, update: Update, context: CallbackContext) -> None:
        """
        SCIPER to kinks.
        """
        update.message.reply_text("This command has been disabled.")
        _, sciper = update.message.text.split(" ", 1)
        try:
            sciper = int(sciper)
            if sciper < 100000 or sciper > 999999:
                raise ValueError
        except ValueError:
            update.message.reply_text("Not a valid SCIPER b-baka.")
            return

        URL = "https://nhentai.to/g/{}".format(sciper)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")

        if soup.title.text == "Not Found":
            update.message.reply_text("{} seems to be pure and innocent...".format(sciper))
            return

        tags = [
            thing
            for thing in soup.findAll("div", {"class": "tag-container"})
            if "Tags" in thing.text
        ]
        if tags:
            tags_text = []
            for tag in [tag.text.strip() for tag in tags[0].findAll("a", {"class": "tag"})]:
                tags_text.append(tag)
            if tags_text:
                update.message.reply_text(
                    "{} is linked to {}.".format(sciper, ", ".join(tags_text))
                )
                return

        update.message.reply_text("{} is a secretive pervert.".format(sciper))

        self.logger.info("{} wants some kinks!".format(update.effective_user.first_name))

    def gender(self, update: Update, context: CallbackContext) -> None:
        """
        PANIK.
        """
        context.bot.forward_message(update.message.chat.id, "59804991", "2626")
        context.bot.forward_message(update.message.chat.id, "59804991", "2627")

        self.logger.info("{} got gendered!".format(update.effective_user.first_name))

    def carpe(self, update: Update, context: CallbackContext) -> None:
        """
        Because no one likes him.
        """
        if update.effective_user.username == "ReallyCrazyMan" and random.randint(1, 6) == 6:
            with open(self._media("opinion.jpg"), "rb") as file:
                update.message.reply_photo(photo=file)

            self.logger.info("{} said ew!".format(update.effective_user.first_name))

    def saisine(self, update: Update, context: CallbackContext) -> None:
        """
        The storm is approaching...
        """
        with open(self._media("saisine.mp3"), "rb") as file:
            update.message.reply_audio(audio=file)

        self.logger.info("{} gets a SAISINE!".format(update.effective_user.first_name))

    def horny(self, update: Update, context: CallbackContext) -> None:
        """
        Vos moeurs toussa.
        """
        context.bot.forward_message(update.message.chat.id, "59804991", "4168")

        self.logger.info("{} found horny!".format(update.effective_user.first_name))

    def crypto(self, update: Update, context: CallbackContext) -> None:
        """
        bullying cryptobros is never unethical.
        """
        context.bot.forward_message(update.message.chat.id, "59804991", "7139").reply_text(
            "(But please don't actually bully people.)"
        )

        self.logger.info("{} wants to bully!".format(update.effective_user.first_name))

    def tiktok(self, update: Update, context: CallbackContext) -> None:
        """
        It is a statement.
        """
        with open(self._media("tiktok.jpg"), "rb") as file:
            update.message.reply_photo(photo=file, caption="choquer decu")

        self.logger.info(
            "{} is asking for cammonte's TikTok!".format(update.effective_user.first_name)
        )

    def stopdoing(self, update: Update, context: CallbackContext) -> None:
        """
        This meme template was supposed to be satire.
        """
        context.bot.forward_message(update.message.chat.id, "59804991", "8467")

        self.logger.info(
            "{} want people to stop doing stop doings!".format(update.effective_user.first_name)
        )

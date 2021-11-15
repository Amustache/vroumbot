import random


from _curses import echo
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
import requests


from ..base import Base


class Text(Base):
    def __init__(self, logger=None):
        commandhandlers = [
            CommandHandler("vroum", self.vroum),
            CommandHandler("vroom", self.vroom),
            CommandHandler(["dad", "dadjoke"], self.dad),
            CommandHandler(["beep", "boop"], self.boop),
            CommandHandler("tut", self.tut),
            CommandHandler(["keysmash", "bottom", "helo"], self.keysmash),
            CommandHandler(["oh", "ooh", "oooh"], self.oh),
            CommandHandler(["ay", "ayy", "ayyy", "xd", "xdd", "xddd"], self.xd),
        ]
        super().__init__(logger, commandhandlers)

    def vroum(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text("Vroum!")

        self.logger.info("{} gets a Vroum!".format(update.effective_user.first_name))

    def vroom(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text("😠")

        self.logger.info("{} gets a 😠!".format(update.effective_user.first_name))

    def dad(self, update: Update, context: CallbackContext) -> None:
        endpoint = "http://dadjokes.online/noecho"
        resp = requests.get(url=endpoint)
        try:
            data = resp.json()
            opener, punchline, _ = data["Joke"].values()
        except:
            update.message.reply_text("No more dad jokes )':.")
            return

        update.message.reply_text(opener).reply_text(punchline)

    def boop(self, update: Update, context: CallbackContext) -> None:
        if "/beep" in update.message.text:
            text = "boop"
        elif "/boop" in update.message.text:
            text = "beep"
        else:
            text = "..."

        update.message.reply_text(text)

        self.logger.info("{} gets a {}!".format(update.effective_user.first_name, text))

    def tut(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text("tut")

        self.logger.info("{} gets a tut!".format(update.effective_user.first_name))

    def keysmash(self, update: Update, context: CallbackContext) -> None:
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

        self.logger.info("{} is keysmashing!".format(update.effective_user.first_name))

    def oh(self, update: Update, context: CallbackContext) -> None:
        mu = 3
        sigma = 2
        length = -1
        while length < 1:
            length = int(random.gauss(mu, sigma))

        result = "o" * length + "h"
        result = "".join([l.upper() if random.randint(1, 6) == 1 else l for l in result])

        update.message.reply_text(result)

        self.logger.info("{} is in awe!".format(update.effective_user.first_name))

    def xd(self, update: Update, context: CallbackContext) -> None:
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

        self.logger.info("{} is in XDing real hard!".format(update.effective_user.first_name))

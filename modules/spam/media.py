import os
import random


from PIL import Image
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


from ..base import Base


class Media(Base):
    def __init__(self, logger=None):
        commandhandlers = [
            CommandHandler(["cat", "chat", "kot"], self.random_cat),
            CommandHandler("brrou", self.brrou),
            CommandHandler("froj", self.froj),
            CommandHandler(["spin", "speen"], self.spin),
            CommandHandler(["saisine", "ccg"], self.saisine),
            CommandHandler("bonjour", self.bonjour),
            CommandHandler("stupid", self.stupid),
            CommandHandler("heretic", self.heretic),
            CommandHandler("bricole", self.bricole),
            CommandHandler("trolled", self.trolled),
            CommandHandler(["nft", "scam"], self.nft),
        ]
        super().__init__(logger, commandhandlers, mediafolder="./media")

    def random_cat(self, update: Update, context: CallbackContext) -> None:
        folder = self._media("cats")
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

        self.logger.info("{} wants a cat pic!".format(update.effective_user.first_name))

    def brrou(self, update: Update, context: CallbackContext) -> None:
        folder = self._media("brrou")
        filename = os.path.join(folder, random.choice(os.listdir(folder)))
        meow = random.choice(["brrou", "Brrou", "b r r o u", "BROU", "B R R O U", "tut"])
        update.message.reply_photo(photo=open(filename, "rb"), caption=meow)

        self.logger.info("{} wants a Brrou pic!".format(update.effective_user.first_name))

    def froj(self, update: Update, context: CallbackContext) -> None:
        folder = self._media("froj")
        filename = os.path.join(folder, random.choice(os.listdir(folder)))
        meow = "https://frogdetective.net/"
        update.message.reply_photo(photo=open(filename, "rb"), caption=meow)

        self.logger.info("{} wants a froj pic!".format(update.effective_user.first_name))

    def spin(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_audio(audio=open(self._media("spin.mp3"), "rb"))

        self.logger.info("{} gets a SPEEN!".format(update.effective_user.first_name))

    def saisine(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_audio(audio=open(self._media("saisine.mp3"), "rb"))

        self.logger.info("{} gets a SAISINE!".format(update.effective_user.first_name))

    def bonjour(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_video(video=open(self._media("setup.mp4"), "rb"))

        self.logger.info("{} gets a bonjour à toutes et tous!".format(update.effective_user.first_name))

    def stupid(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_video(video=open(self._media("stupid.mp4"), "rb"))

        self.logger.info("{} is being really stupid right now!".format(update.effective_user.first_name))

    def heretic(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_video(video=open(self._media("heretic.mp4"), "rb"))

        self.logger.info("{} likes being a heretic!".format(update.effective_user.first_name))

    def bricole(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_video(video=open(self._media("bricole.mp4"), "rb"))

        self.logger.info("{} wants to BRICOLE!".format(update.effective_user.first_name))

    def trolled(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_video(video=open(self._media("troll.mp4"), "rb"))

        self.logger.info("{}'s just been trolled!".format(update.effective_user.first_name))

    def nft(self, update: Update, context: CallbackContext) -> None:
        if update.message.reply_to_message:
            user = update.message.reply_to_message.from_user
        else:
            user = update.effective_user

        userid = user.id

        filename = os.path.join(self._media("nft"), "{}.png".format(userid))

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

        self.logger.info("{} now has an NFT!".format(user.first_name))

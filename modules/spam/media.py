"""
Media spam! Yay!
"""
import imp
from typing import Tuple
from urllib.request import urlopen
import json
import os
import random


from PIL import Image
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


from ..base import Base


class Media(Base):
    """
    Media spam! Yay!
    """

    def __init__(self, logger=None):
        commandhandlers = [
            CommandHandler(["cat", "chat", "kot"], self.random_cat),
            CommandHandler("brrou", self.brrou),
            CommandHandler("froj", self.froj),
            CommandHandler(["spin", "speen"], self.spin),
            CommandHandler("bonjour", self.bonjour),
            CommandHandler("stupid", self.stupid),
            CommandHandler("heretic", self.heretic),
            CommandHandler("bricole", self.bricole),
            CommandHandler("trolled", self.trolled),
            CommandHandler(["nft", "scam"], self.nft),
            CommandHandler(["pointeur", "baisepointeur"], self.pointeur),
            CommandHandler(["dum", "dumb"], self.dumb),
            CommandHandler(["srydum", "sorrydumb", "sorrydum", "srydumb"], self.sorrydumb),
            CommandHandler(["dog", "woof", "dogo", "doggo"], self.random_dog),
            CommandHandler("misty", self.misty),
        ]
        super().__init__(logger, commandhandlers, mediafolder="./media")

    def random_cat(self, update: Update, context: CallbackContext) -> None:
        """
        Random cat from a (currated) list.
        """
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
        if random.randint(1, 6) > 3:
            folder = self._media("cats")
            filename = os.path.join(folder, random.choice(os.listdir(folder)))
            with open(filename, "rb") as file:
                update.message.reply_photo(photo=file, caption=meow)
        else:
            url = "https://api.thecatapi.com/v1/images/search"
            response = urlopen(url)
            data_json = json.loads(response.read())
            update.message.reply_photo(photo=data_json[0]["url"], caption=meow)

        self.logger.info("{} wants a cat pic!".format(update.effective_user.first_name))

    def brrou(self, update: Update, context: CallbackContext) -> None:
        """
        A very special cat.
        """
        folder = self._media("brrou")
        filename = os.path.join(folder, random.choice(os.listdir(folder)))
        meow = random.choice(["brrou", "Brrou", "b r r o u", "BROU", "B R R O U", "tut"])
        with open(filename, "rb") as file:
            update.message.reply_photo(photo=file, caption=meow)

        self.logger.info("{} wants a Brrou pic!".format(update.effective_user.first_name))

    def froj(self, update: Update, context: CallbackContext) -> None:
        """
        FROJ
        """
        folder = self._media("froj")
        filename = os.path.join(folder, random.choice(os.listdir(folder)))
        meow = "https://frogdetective.net/"
        with open(filename, "rb") as file:
            update.message.reply_photo(photo=file, caption=meow)

        self.logger.info("{} wants a froj pic!".format(update.effective_user.first_name))

    def spin(self, update: Update, context: CallbackContext) -> None:
        """
        SPIN
        """
        with open(self._media("spin.mp3"), "rb") as file:
            update.message.reply_audio(audio=file)

        self.logger.info("{} gets a SPEEN!".format(update.effective_user.first_name))

    def bonjour(self, update: Update, context: CallbackContext) -> None:
        """
        BONJOUR A TOUTES ET TOUT
        """
        with open(self._media("setup.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info(
            "{} gets a bonjour à toutes et tous!".format(update.effective_user.first_name)
        )

    def stupid(self, update: Update, context: CallbackContext) -> None:
        """
        A little song for a little dumb
        """
        with open(self._media("stupid.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info(
            "{} is being really stupid right now!".format(update.effective_user.first_name)
        )

    def heretic(self, update: Update, context: CallbackContext) -> None:
        """
        HERESY TIME
        """
        with open(self._media("heretic.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info("{} likes being a heretic!".format(update.effective_user.first_name))

    def bricole(self, update: Update, context: CallbackContext) -> None:
        """
        Best song
        """
        with open(self._media("bricole.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info("{} wants to BRICOLE!".format(update.effective_user.first_name))

    def trolled(self, update: Update, context: CallbackContext) -> None:
        """
        A little song when someone gets trolled
        """
        with open(self._media("troll.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info("{}'s just been trolled!".format(update.effective_user.first_name))

    def nft(self, update: Update, context: CallbackContext) -> None:
        import random



        """
        Your very own NFT!
        """
        if update.message.reply_to_message:
            user = update.message.reply_to_message.from_user
        else:
            user = update.effective_user

        userid = user.id


        filename = os.path.join(self._media("nft"), "{}.png".format(userid))

        if not os.path.isfile(filename):
            random.seed(userid)
            r_color = lambda: (random.randint(0,255), random.randint(0,255), random.randint(0,255), int(255))
            black = (0, 0, 0, 255)

            colors = [r_color(), r_color(), r_color(), black, black, black]

            binuserid = bin(userid)[2:].zfill(64)

            vroumbot = "vroumbot"
            binvroumbot = "".join(format(ord(x), "b").zfill(8) for x in vroumbot)

            img = Image.new("RGBA", (32, 32), "black")
            
            pixels = img.load()

            for i in range(2, img.size[0] // 2):
                for j in range(2, img.size[1] - 2):
                    c = random.choice(colors)
                    pixels[i, j] = c
                    pixels[img.size[0] - i -1, j] = c

            img.resize((512, 512), Image.NEAREST).save(filename)

        with open(filename, "rb") as file:
            update.message.reply_photo(
                photo=file,
                caption="This is {}'s exclusive NFT, do not use without permission!".format(
                    user.first_name
                ),
            )

        self.logger.info("{} now has an NFT!".format(user.first_name))

    def pointeur(self, update: Update, context: CallbackContext) -> None:
        """
        Ici,on baise tous les pointeurs.
        """
        with open(self._media("pointeur.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info("{} baise tous les pointeurs!".format(update.effective_user.first_name))

    def dumb(self, update: Update, context: CallbackContext) -> None:
        """
        You are dumb in harmonic.
        """
        with open(self._media("dumb.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info("{} is calling someone dumb!".format(update.effective_user.first_name))

    def sorrydumb(self, update: Update, context: CallbackContext) -> None:
        """
        Sorry to calling you dumb in harmonic.
        """
        with open(self._media("sorrydumb.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info(
            "{} is sorry for calling someone dumb!".format(update.effective_user.first_name)
        )

    def random_dog(self, update: Update, context: CallbackContext) -> None:
        """
        Random dog from API.
        """
        woof = random.choice(
            [
                "woof woof",
                "ruff ruff",
                "arf arf",
                "bow wow",
                "yap yap",
                "yip yip",
                "wuff wuff",
                "wau wau",
                "hev hev",
                "hav hav",
                "guau guau",
                "gua gua",
                "jau jau",
                "blaf blaf",
                "woef woef",
                "keff keff",
                "гав гав",
                "тяв тяв",
                "멍멍",
                "ワンワン",
                "キャンキャン",
                "gav gav",
                "tyav  tyav ",
                "meong meong",
                "wan wan ",
                "kyan kyan",
                "bau bau",
                "bow bow",
                "voff voff",
                "blaf blaf",
                "kef kef",
                "waf waf",
                "woef woef",
                "vov vov",
                "vuf vuf",
                "wang wang",
                "汪汪",
                "ham ham",
                "waouh waouh",
                "ouah ouah",
                "ouaf ouaf",
                "vaf vaf",
                "wouf wouf",
                "wouaf wouaf",
                "jappe jappe",
            ]
        )
        url = "https://api.thedogapi.com/v1/images/search"
        response = urlopen(url)
        data_json = json.loads(response.read())
        update.message.reply_photo(photo=data_json[0]["url"], caption=woof)

        self.logger.info("{} wants a dog pic!".format(update.effective_user.first_name))

    def misty(self, update: Update, context: CallbackContext) -> None:
        """
        A very special dog.
        """
        folder = self._media("misty")
        filename = os.path.join(folder, random.choice(os.listdir(folder)))
        meow = random.choice(["misty", "Misty", "MISTY", "... Misty?", "Misty!", "Mistyyy"])
        with open(filename, "rb") as file:
            update.message.reply_photo(photo=file, caption=meow)

        self.logger.info("{} wants a Misty pic!".format(update.effective_user.first_name))

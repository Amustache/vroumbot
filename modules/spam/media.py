"""
Media spam! Yay!
"""
from urllib.request import urlopen
import html
import json
import os
import random


from PIL import Image
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
import requests


from ..base import Base, command_enabled


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
            CommandHandler(["trolled", "cliquesurmoi", "playsound"], self.trolled),
            CommandHandler(["nft", "scam"], self.nft),
            CommandHandler(["generative"], self.randompic),
            CommandHandler(["pointeur", "baisepointeur"], self.pointeur),
            CommandHandler(["dum", "dumb"], self.dumb),
            CommandHandler(["srydum", "sorrydumb", "sorrydum", "srydumb"], self.sorrydumb),
            CommandHandler(["dog", "woof", "dogo", "doggo"], self.random_dog),
            CommandHandler("misty", self.misty),
            CommandHandler(["xkcd", "insertRelevantXKCDComicHere"], self.xkcd),
            CommandHandler("funny", self.funny),
            CommandHandler(["gm", "goodmorning"], self.gm),
            CommandHandler("spam", self.spam),
            CommandHandler(["enretard", "retard"], self.enretard),
            CommandHandler("repo", self.repo),
            CommandHandler(["speedrun", "summoningsalt"], self.speedrun),
        ]
        super().__init__(logger, commandhandlers, mediafolder="./media")

    @command_enabled(default=True)
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

        self.logger.info(f"{update.effective_user.first_name} wants a cat pic!")

    @command_enabled(default=True)
    def brrou(self, update: Update, context: CallbackContext) -> None:
        """
        A very special cat.
        """
        folder = self._media("brrou")
        filename = os.path.join(folder, random.choice(os.listdir(folder)))
        meow = random.choice(["brrou", "Brrou", "b r r o u", "BROU", "B R R O U", "tut"])
        with open(filename, "rb") as file:
            update.message.reply_photo(photo=file, caption=meow)

        self.logger.info(f"{update.effective_user.first_name} wants a Brrou pic!")

    @command_enabled(default=False)
    def froj(self, update: Update, context: CallbackContext) -> None:
        """
        FROJ
        """
        folder = self._media("froj")
        filename = os.path.join(folder, random.choice(os.listdir(folder)))
        meow = "https://frogdetective.net/"
        with open(filename, "rb") as file:
            update.message.reply_photo(photo=file, caption=meow)

        self.logger.info(f"{update.effective_user.first_name} wants a froj pic!")

    @command_enabled(default=False)
    def spin(self, update: Update, context: CallbackContext) -> None:
        """
        SPIN
        """
        with open(self._media("spin.mp3"), "rb") as file:
            update.message.reply_audio(audio=file)

        self.logger.info(f"{update.effective_user.first_name} gets a SPEEN!")

    @command_enabled(default=False)
    def bonjour(self, update: Update, context: CallbackContext) -> None:
        """
        BONJOUR A TOUTES ET TOUT
        """
        with open(self._media("setup.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info(f"{update.effective_user.first_name} gets a bonjour à toutes et tous!")

    @command_enabled(default=False)
    def stupid(self, update: Update, context: CallbackContext) -> None:
        """
        A little song for a little dumb
        """
        with open(self._media("stupid.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info(f"{update.effective_user.first_name} is being really stupid right now!")

    @command_enabled(default=False)
    def heretic(self, update: Update, context: CallbackContext) -> None:
        """
        HERESY TIME
        """
        with open(self._media("heretic.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info(f"{update.effective_user.first_name} likes being a heretic!")

    @command_enabled(default=False)
    def bricole(self, update: Update, context: CallbackContext) -> None:
        """
        Best song
        """
        with open(self._media("bricole.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info(f"{update.effective_user.first_name} wants to BRICOLE!")

    @command_enabled(default=False)
    def trolled(self, update: Update, context: CallbackContext) -> None:
        """
        A little song when someone gets trolled
        """
        with open(self._media("troll.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info(f"{update.effective_user.first_name}'s just been trolled!")

    @command_enabled(default=False)
    def nft(self, update: Update, context: CallbackContext) -> None:
        """
        Your very own NFT!
        """
        if update.message.reply_to_message:
            user = update.message.reply_to_message.from_user
        else:
            user = update.effective_user

        userid = user.id

        filename = os.path.join(self._media("nft"), f"{userid}.png")

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

        with open(filename, "rb") as file:
            update.message.reply_photo(
                photo=file,
                caption=f"This is {user.first_name}'s exclusive NFT, do not use without permission!",
            )

        self.logger.info(f"{user.first_name} now has an NFT!")

    @command_enabled(default=False)
    def randompic(self, update: Update, context: CallbackContext) -> None:
        """
        Your very own generative art piece!
        """
        if update.message.reply_to_message:
            user = update.message.reply_to_message.from_user
        else:
            user = update.effective_user

        userid = user.id

        filename = os.path.join(self._media("randompic"), f"{userid}.png")

        if not os.path.isfile(filename):
            random.seed(userid)
            r_color = lambda: (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                int(255),
            )
            black = (0, 0, 0, 255)

            colors = [r_color(), r_color(), r_color(), black, black, black]

            if len(context.args) >= 1:
                img_size = context.args[0]
            else:
                img_size = 32

            try:
                img_size = int(img_size)
                if img_size < 8:
                    update.message.reply_text(
                        "Don't toy with the bot! Enter a valid integer between 8 and 512."
                    )
                    return

                if img_size > 512:
                    update.message.reply_text(
                        "Don't toy with the bot! Enter a valid integer between 8 and 512."
                    )
                    return

            except:
                update.message.reply_text(
                    "Don't toy with the bot! Enter a valid integer between 8 and 512."
                )
                return

            img = Image.new("RGBA", (img_size, img_size), "black")

            pixels = img.load()

            for i in range(2, img.size[0] // 2):
                for j in range(2, img.size[1] - 2):
                    c = random.choice(colors)
                    pixels[i, j] = c
                    pixels[img.size[0] - i - 1, j] = c

            img.resize((512, 512), Image.NEAREST).save(filename)

        with open(filename, "rb") as file:
            update.message.reply_photo(
                photo=file,
                caption=f"This is {user.first_name}'s exclusive generative art piece",
            )
        self.logger.info(f"{user.first_name} wants a random pic!")

    @command_enabled(default=False)
    def pointeur(self, update: Update, context: CallbackContext) -> None:
        """
        Ici,on baise tous les pointeurs.
        """
        with open(self._media("pointeur.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info(f"{update.effective_user.first_name} baise tous les pointeurs!")

    @command_enabled(default=False)
    def dumb(self, update: Update, context: CallbackContext) -> None:
        """
        You are dumb in harmonic.
        """
        with open(self._media("dumb.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info(f"{update.effective_user.first_name} is calling someone dumb!")

    @command_enabled(default=False)
    def sorrydumb(self, update: Update, context: CallbackContext) -> None:
        """
        Sorry to calling you dumb in harmonic.
        """
        with open(self._media("sorrydumb.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info(f"{update.effective_user.first_name} is sorry for calling someone dumb!")

    @command_enabled(default=False)
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

        self.logger.info(f"{update.effective_user.first_name} wants a dog pic!")

    @command_enabled(default=False)
    def misty(self, update: Update, context: CallbackContext) -> None:
        """
        A very special dog.
        """
        folder = self._media("misty")
        filename = os.path.join(folder, random.choice(os.listdir(folder)))
        meow = random.choice(["misty", "Misty", "MISTY", "... Misty?", "Misty!", "Mistyyy"])
        with open(filename, "rb") as file:
            update.message.reply_photo(photo=file, caption=meow)

        self.logger.info(f"{update.effective_user.first_name} wants a Misty pic!")

    @command_enabled(default=True)
    def xkcd(self, update: Update, context: CallbackContext) -> None:
        """
        Random XKCD
        """
        try:
            _, args = update.message.text.split(" ", 1)
        except ValueError:
            args = None

        if args:
            try:
                num = int(args)
            except ValueError:
                num = None

            # If number provided, selected comic
            if num:
                try:
                    url = f"https://xkcd.com/{num}/info.0.json"
                    response = urlopen(url)
                    data_json = json.loads(response.read())
                    update.message.reply_photo(
                        photo=data_json["img"],
                        caption=f"XKCD #{num}: {data_json['safe_title']}\n\n{data_json['alt']}",
                    )
                except:
                    update.message.reply_text("This XKCD does not exists :/")
            # If string provided, search
            else:
                args_safe = html.escape(args)
                try:
                    url = "https://relevant-xkcd-backend.herokuapp.com/search"
                    myobj = {"search": args_safe}
                    response = requests.post(url, data=myobj)
                    results = json.loads(response.text)["results"]
                except:
                    update.message.reply_text("An error has occured :/")
                    return
                text = f'Results for "{args}" ({len(results)} found):\n'
                for result in results:
                    text += "- {result['number']}: {result['title']} ({result['url']})\n"
                update.message.reply_text(text, disable_web_page_preview=True)
        # No args == Random comic
        else:
            url_last = "https://xkcd.com/info.0.json"
            response = urlopen(url_last)
            data_json = json.loads(response.read())
            max = data_json["num"]
            num = random.randint(1, max)

            # We test for existence
            ok = False
            while not ok:
                try:
                    num = random.randint(1, max)
                    url = f"https://xkcd.com/{num}/info.0.json"
                    response = urlopen(url)
                    data_json = json.loads(response.read())
                    ok = True
                except:
                    ok = False

            update.message.reply_photo(
                photo=data_json["img"],
                caption=f"XKCD #{num}: {data_json['safe_title']}\n\n{data_json['alt']}",
            )

        self.logger.info(f"{update.effective_user.first_name} wants some XKCD!")

    @command_enabled(default=False)
    def funny(self, update: Update, context: CallbackContext) -> None:
        """
        That's funny
        """
        with open(self._media("funny.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info(f"{update.effective_user.first_name}'s found something funny!")

    @command_enabled(default=False)
    def gm(self, update: Update, context: CallbackContext) -> None:
        """
        Good morning y'all!
        """
        with open(self._media("gm.mp4"), "rb") as file:
            update.message.reply_text("Good morning y'all!").reply_video(video=file)

        self.logger.info(f"{update.effective_user.first_name}'s says good morning y'all!")

    @command_enabled(default=True)
    def spam(self, update: Update, context: CallbackContext) -> None:
        """
        Because, y'know. Guns kill people.
        """
        with open(self._media("spam.jpg"), "rb") as file:
            update.message.reply_photo(photo=file)

        self.logger.info(f"{update.effective_user.first_name} calls for spam!")

    @command_enabled(default=False)
    def enretard(self, update: Update, context: CallbackContext) -> None:
        """
        When someone is late for a meeting.
        """
        with open(self._media("enretard.mp4"), "rb") as file:
            update.message.reply_video(video=file)

        self.logger.info(f"{update.effective_user.first_name}'s says that someone is late!")

    @command_enabled(default=False)
    def repo(self, update: Update, context: CallbackContext) -> None:
        """
        GIV REPO
        """
        with open(self._media("repo.jpg"), "rb") as file:
            update.message.reply_photo(photo=file)

        self.logger.info(f"{update.effective_user.first_name} wants your repo!")

    @command_enabled(default=False)
    def speedrun(self, update: Update, context: CallbackContext) -> None:
        """
        Speedrun time.
        """
        with open(self._media("HOME_Were_Finally_Landing.mp3"), "rb") as file:
            update.message.reply_audio(audio=file)

        self.logger.info(f"{update.effective_user.first_name} is ready for a speedrun!")

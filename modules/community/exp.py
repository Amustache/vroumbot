import ast
import os


from PIL import Image, ImageDraw, ImageFont
from telegram import ForceReply, Update
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, Filters, MessageHandler


from secret import BOT_ID


from ..base import Base
from .helpers import deobfuscate, get_user


def needed_exp(level, karma):
    if level == 0:
        return 0
    # Dirty hack
    if level == 1:
        return 5
    return int((level ** 3.14) * (1 - (karma / (level ** 3.14))))


GENDER, PHOTO, LOCATION, BIO = range(4)


class Exp(Base):
    def __init__(self, logger=None, table=None):
        commandhandlers = [
            MessageHandler(~Filters.command, self.add_message),
            CommandHandler(["level", "mylevel"], self.get_level),
            CommandHandler(["levels", "leaderboard"], self.get_leaderboard),
            CommandHandler(["reset_levels"], self.reset_from_history),
        ]
        super().__init__(logger, commandhandlers, table, mediafolder="./media/exp")

    def add_message(self, update: Update, context: CallbackContext):
        user = update.effective_user
        dbuser = get_user(self.table, user.id, update.message.chat.id)
        dbuser.num_messages += 1
        dbuser.userfirstname = user.first_name

        change = dbuser.level
        while dbuser.num_messages > needed_exp(dbuser.level, dbuser.karma):
            dbuser.level += 1

        if change != dbuser.level:
            filename = os.path.join(self._media("basis"), "({}).png".format(dbuser.level))
            with Image.open(filename).convert("RGBA") as image:
                font_path = self._media("ReemKufi-Regular.ttf")
                d1 = ImageDraw.Draw(image)

                # Icon
                icon = Image.open(self._media("icons/stonks.png")).convert("RGBA")
                image.paste(icon, box=(45, 46), mask=icon)  # hardcoded

                # Title
                font = ImageFont.truetype(font_path, 70)  # hardcoded
                d1.text((178, 0), "Level Up!", font=font, fill=(0, 0, 0))

                # Info
                text = "{} is now Level {}".format(dbuser.userfirstname, dbuser.level)
                fontsize = 1
                font = ImageFont.truetype(font_path, fontsize)
                while font.getsize(text)[0] < 575:  # hardcoded
                    fontsize += 1
                    font = ImageFont.truetype(font_path, fontsize)
                d1.text((178, 90), text, font=font, fill=(0, 0, 0))  # hardcoded

                image.save("temp.webp", "WEBP")

            with open("temp.webp", "rb") as file:
                update.message.reply_document(
                    document=file,
                    caption="📈 LEVEL UP 📈!\n{} is now Level {}!".format(
                        dbuser.userfirstname, dbuser.level
                    ),
                )

            os.remove("temp.webp")

        dbuser.save()

    def get_level(self, update: Update, context: CallbackContext):
        if update.message.reply_to_message:
            user = update.message.reply_to_message.from_user
            if user.id == BOT_ID:
                update.message.reply_text("I don't level up, silly ~")
                return
            dbuser = get_user(self.table, user.id, update.message.chat.id)
        else:
            user = update.effective_user
            dbuser = get_user(self.table, user.id, update.message.chat.id)
        dbuser.userfirstname = user.first_name

        filename = os.path.join(self._media("basis"), "({}).png".format(dbuser.level))
        with Image.open(filename).convert("RGBA") as image:
            font_path = self._media("ReemKufi-Regular.ttf")
            d1 = ImageDraw.Draw(image)

            # Icon
            icon = Image.open(self._media("icons/info.png")).convert("RGBA")
            image.paste(icon, box=(45, 46), mask=icon)  # hardcoded

            # Title
            fontsize = 70  # hardcoded
            font = ImageFont.truetype(font_path, fontsize)
            while font.getsize(dbuser.userfirstname)[0] > 575:  # hardcoded
                fontsize -= 1
                font = ImageFont.truetype(font_path, fontsize)
            d1.text((178, 0), dbuser.userfirstname, font=font, fill=(0, 0, 0))

            # Info
            text = "Level {} ({} msg, {} krm)".format(
                dbuser.level, dbuser.num_messages, dbuser.karma
            )
            fontsize = 1
            font = ImageFont.truetype(font_path, fontsize)
            while font.getsize(text)[0] < 575:  # hardcoded
                fontsize += 1
                font = ImageFont.truetype(font_path, fontsize)
            d1.text((178, 90), text, font=font, fill=(0, 0, 0))  # hardcoded

            image.save("temp.webp", "WEBP")

        with open("temp.webp", "rb") as file:
            update.message.reply_document(
                document=file,
                caption="📈 LEVEL UP 📈!\n{} is now Level {}!".format(
                    dbuser.userfirstname, dbuser.level
                ),
            )

        os.remove("temp.webp")

        dbuser.save()

    def get_leaderboard(self, update: Update, context: CallbackContext):
        try:
            _, num_people = update.message.text.split(" ", 1)
            num_people = int(num_people)
            if num_people < 1:
                num_people = 10
        except ValueError:
            num_people = 10

        users = (
            self.table.select()
            .where(self.table.chatid == update.message.chat.id)
            .order_by(self.table.level.desc())
            .order_by(self.table.num_messages.desc())
            .limit(num_people)
        )

        levels = {
            user.userid: [user.userfirstname, user.level, user.num_messages] for user in users
        }
        try:
            _ = levels.pop(BOT_ID)
        except:
            pass
        num_people = min(len(levels), num_people)

        all_people = []
        for i, (userid, data) in enumerate(levels.items()):
            if i < num_people:
                username, level, num_messages = data
                if not username:
                    username = "<No registered username>"
                    dbuser = get_user(self.table, userid, update.message.chat.id)
                    while dbuser.num_messages > needed_exp(dbuser.level, dbuser.karma):
                        dbuser.level += 1
                    level = dbuser.level
                    dbuser.save()
                all_people.append(
                    "{}. {}: level {} ({} messages).".format(i + 1, username, level, num_messages)
                )
            else:
                break

        update.message.reply_text("\n".join(all_people))

    def reset_from_history(self, update: Update, context: CallbackContext):
        try:
            data = ast.literal_eval(deobfuscate(context.args[0]))
            update.message.delete()
            for userid, num_messages in data.items():
                dbuser = get_user(self.table, userid, update.message.chat.id)
                dbuser.num_messages = num_messages
                dbuser.save()
            update.message.reply_text("Levels updated.")
        except (ValueError, IndexError):
            update.message.delete()
            update.message.reply_text("Error while updating levels.")

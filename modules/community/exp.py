"""
Level up, baby!
"""
import ast
import os


from PIL import Image, ImageDraw, ImageFont
from telegram import ForceReply, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, Filters, MessageHandler


from secret import BOT_ID


from ..base import admin_only, Base, command_enabled
from .helpers import deobfuscate, get_user, obfuscate


def needed_exp(level, karma):
    if level == 0:
        return 0
    # Dirty hack
    if level == 1:
        return 5
    return int((level**3.14) * (1 - (karma / (level**3.14))))


class Exp(Base):
    """
    Level up, baby!
    """

    def __init__(self, logger=None, table=None):
        commandhandlers = [
            MessageHandler(~Filters.command, self.add_message),
            CommandHandler(["levelup", "levelupdate"], self.levelup_update),
            CommandHandler(["level", "mylevel"], self.get_level),
            CommandHandler(["levels", "leaderboard"], self.get_leaderboard),
            CommandHandler(["reset_levels"], self.reset_from_history),
            MessageHandler(Filters.document, self.get_obfuscated_history),
        ]
        super().__init__(logger, commandhandlers, table, mediafolder="./media/exp")

    def _generate_pic(self, username, level, text, pic):
        filename = os.path.join(self._media("basis"), f"({level}).png")

        with Image.open(filename).convert("RGBA") as image:
            picname = self._media("temp.webp")

            font_path = self._media("ReemKufi-Regular.ttf")
            d1 = ImageDraw.Draw(image)

            # Icon
            icon = Image.open(self._media(f"icons/{pic}.png")).convert("RGBA")
            image.paste(icon, box=(45, 46), mask=icon)  # hardcoded

            # Title
            fontsize = 70  # hardcoded
            font = ImageFont.truetype(font_path, fontsize)
            while font.getsize(username)[0] > 575:  # hardcoded
                fontsize -= 1
                font = ImageFont.truetype(font_path, fontsize)
            d1.text((178, 0), username, font=font, fill=(0, 0, 0))

            # Info
            fontsize = 1
            font = ImageFont.truetype(font_path, fontsize)
            while font.getsize(text)[0] < 575:  # hardcoded
                fontsize += 1
                font = ImageFont.truetype(font_path, fontsize)
            d1.text((178, 90), text, font=font, fill=(0, 0, 0))  # hardcoded

            image.save(picname, "WEBP")

            return picname

    @command_enabled(default=True)
    def levelup_update(self, update: Update, context: CallbackContext):
        """
        Placeholder function to send a level update (basically used to disable firing the levelup pic).
        """
        user = update.effective_user
        dbuser = get_user(self.table, user.id, update.message.chat.id)

        # GDPR
        if not dbuser:
            return

        text = f"{dbuser.userfirstname} is now Level {dbuser.level}"
        picname = self._generate_pic(dbuser.userfirstname, dbuser.level, text, "stonks")

        with open(picname, "rb") as file:
            update.message.reply_document(
                document=file,
                caption=text,
            )

        os.remove(picname)

    def add_message(self, update: Update, context: CallbackContext):
        """
        Basically count the messages and send update.
        """
        user = update.effective_user
        dbuser = get_user(self.table, user.id, update.message.chat.id)

        # GDPR
        if not dbuser:
            return

        dbuser.num_messages += 1
        dbuser.userfirstname = user.first_name

        change = dbuser.level
        while dbuser.num_messages > needed_exp(dbuser.level, dbuser.karma):
            dbuser.level += 1

        dbuser.save()

        if change != dbuser.level:
            self.levelup_update(update, context)

    @command_enabled(default=True)
    def get_level(self, update: Update, context: CallbackContext):
        """
        Get users levels.
        """
        if update.message.reply_to_message:
            user = update.message.reply_to_message.from_user
            if user.id == BOT_ID:
                update.message.reply_text("I don't level up, silly ~")
                return
            dbuser = get_user(self.table, user.id, update.message.chat.id)
        else:
            user = update.effective_user
            dbuser = get_user(self.table, user.id, update.message.chat.id)

        # GDPR
        if not dbuser:
            return

        dbuser.userfirstname = user.first_name

        text = f"Level {dbuser.level} ({dbuser.num_messages} msg, {dbuser.karma} krm)"
        picname = self._generate_pic(dbuser.userfirstname, dbuser.level, text, "info")

        with open(picname, "rb") as file:
            update.message.reply_document(
                document=file,
                caption=text,
            )

        os.remove(picname)

        dbuser.save()

    @command_enabled(default=True)
    def get_leaderboard(self, update: Update, context: CallbackContext):
        """
        Get users leaderboard.
        """
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
            user.userid: [user.userfirstname, user.level, user.num_messages, user.karma]
            for user in users
        }
        try:
            _ = levels.pop(BOT_ID)
        except KeyError:  # Not the correct bot
            pass
        num_people = min(len(levels), num_people)

        all_people = []
        for i, (userid, data) in enumerate(levels.items()):
            if i < num_people:
                username, level, num_messages, karma = data
                if level > 0:
                    if not username:
                        username = "<No registered username>"
                        dbuser = get_user(self.table, userid, update.message.chat.id)
                        while dbuser.num_messages > needed_exp(dbuser.level, dbuser.karma):
                            dbuser.level += 1
                        level = dbuser.level
                        dbuser.save()
                    all_people.append(
                        f"{i + 1}. {username}: Level {level} ({num_messages} msg, {karma} krm)."
                    )
            else:
                break

        if all_people:
            update.message.reply_text("\n".join(all_people))
        else:
            update.message.reply_text("No one talked yet... ):")

    @admin_only
    def reset_from_history(self, update: Update, context: CallbackContext):
        """
        Reset based on a groupchat export.
        """
        try:
            data = ast.literal_eval(deobfuscate(context.args[0]))
            try:
                update.message.delete()
            except BadRequest:
                update.message.reply_text("Bot is not admin, please delete the message manually.")
            for userid, num_messages in data.items():
                if userid == BOT_ID:
                    continue
                dbuser = get_user(self.table, userid, update.message.chat.id)
                dbuser.num_messages = num_messages
                while dbuser.num_messages > needed_exp(dbuser.level, dbuser.karma):
                    dbuser.level += 1
                dbuser.save()
        except (ValueError, IndexError) as e:
            print(e)
            update.message.reply_text(
                "Error while updating levels.\n\n"
                "Need help? Refer to the wiki!\n"
                "https://github.com/Amustache/vroumbot/wiki"
            )

    @admin_only
    def get_obfuscated_history(self, update: Update, context: CallbackContext):
        """
        Get obfuscated history based on a file.
        """
        with open("temp.json", "w+") as f:
            context.bot.get_file(update.message.document).download(out=f)
            text = obfuscate("".join(f.read().split()))
            update.message.reply_text("Send that text as argument for /reset_from_history:")
            update.message.reply_text(text)

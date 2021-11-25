"""
Karma module is used to handle karma in groupchats.
"""
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


from .base import Base


class Karma(Base):
    """
    Karma module is used to handle karma in groupchats.
    """

    def __init__(self, logger=None, table=None):
        commandhandlers = [
            CommandHandler(["plus", "pos", "bravo"], self.plus),
            CommandHandler(["angryplus", "angrypos", "angrybravo", "angry"], self.angryplus),
            CommandHandler(["moins", "minus", "min", "neg", "non"], self.moins),
            CommandHandler(["karma", "getkarma"], self.getkarma),
        ]
        super().__init__(logger, commandhandlers, table)

    def _get_user(self, userid, chatid):
        """
        Return the user from the database.
        :param userid: Telegram userid.
        :param chatid: Telegram chatid.
        :return: Model: User
        """
        user, _ = self.table.get_or_create(userid=userid, chatid=chatid)

        return user

    def _get_karma(self, chatid):
        """
        List all karma scores from a chat.
        :param chatid: Telegram chatid.
        :return: {user_id: Int: [user_firstname: String, user_karma: Int]}
        """
        users = (
            self.table.select().where(self.table.chatid == chatid).order_by(self.table.karma.desc())
        )

        return {user.userid: [user.userfirstname, user.karma] for user in users}

    def plus(self, update: Update, context: CallbackContext) -> None:
        """
        Add karma to user by replying to a message.
        """
        if update.message.reply_to_message:
            user = update.message.reply_to_message.from_user
            dbuser = self._get_user(user.id, update.message.chat.id)

            if user == update.effective_user:
                update.message.reply_text("Humble bragging, amarite?")
                self.logger.info("{} wants to pos themselves!".format(user.first_name))

            else:
                dbuser.karma += 1
                update.message.reply_to_message.reply_text(
                    "+1 for {} ({} points).".format(user.first_name, dbuser.karma)
                )
                self.logger.info("{} gets a +1!".format(user.first_name))

            dbuser.userfirstname = user.first_name
            dbuser.save()
        else:
            update.message.reply_text("You must respond to a message to give karma.")

    def angryplus(self, update: Update, context: CallbackContext) -> None:
        self.plus(update, context)
        if update.message.reply_to_message:
            with open(self._media("angrypos.jpg"), "rb") as file:
                update.message.reply_audio(audio=file)

                self.logger.info("{} gets an angry +1!".format(update.effective_user.first_name))

    def moins(self, update: Update, context: CallbackContext) -> None:
        """
        Remove karma to user by replying to a message.
        """
        if update.message.reply_to_message:
            user = update.message.reply_to_message.from_user
            dbuser = self._get_user(user.id, update.message.chat.id)

            if user == update.effective_user:
                update.message.reply_text("Don't be so harsh on yourself.")
                self.logger.info("{} wants to neg themselves!".format(user.first_name))

            else:
                dbuser.karma -= 1
                update.message.reply_to_message.reply_text(
                    "-1 for {} ({} points).".format(user.first_name, dbuser.karma)
                )
                self.logger.info("{} gets a -1!".format(user.first_name))

            dbuser.userfirstname = user.first_name
            dbuser.save()
        else:
            update.message.reply_text("You must respond to a message to give karma.")

    def getkarma(self, update: Update, context: CallbackContext) -> None:
        """
        Give the karma score for a user by replying, or karma scores from a chat.
        """
        if update.message.reply_to_message:
            user = update.message.reply_to_message.from_user
            dbuser = self._get_user(user.id, update.message.chat.id)
            dbuser.userfirstname = user.first_name
            dbuser.save()

            update.message.reply_text(
                "{} has {} points.".format(dbuser.userfirstname, dbuser.karma)
            )
            self.logger.info("{} has {} karma!".format(dbuser.userfirstname, dbuser.karma))

        else:
            try:
                _, num_people = update.message.text.split(" ", 1)
                num_people = int(num_people)
                if num_people < 1:
                    num_people = 10
            except ValueError:
                num_people = 10

            karmas = self._get_karma(update.message.chat.id)
            num_people = min(len(karmas), num_people)

            all_people = []
            for i, (_, data) in enumerate(karmas.items()):
                if i < num_people:
                    username, karma = data
                    if not username:
                        username = "<please trigger karma action for name>"
                    if karma != 0:
                        all_people.append("{}. {}: {} points.".format(i + 1, username, karma))
                else:
                    break

            update.message.reply_text("\n".join(all_people))
            self.logger.info(
                "{} wants to know the karmas!".format(update.effective_user.first_name)
            )

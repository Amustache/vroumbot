"""
Karma module is used to handle karma in groupchats.
"""
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


from ..base import Base
from .helpers import get_user


angrypos_commands = ["angryplus", "angrypos", "angrybravo", "angry"]
pos_commands = ["plus", "pos", "bravo"]
neg_commands = ["moins", "minus", "min", "neg", "non"]
meh_commands = ["meh"]

class Karma(Base):
    """
    Karma module is used to handle karma in groupchats.
    """

    def __init__(self, logger=None, table=None):
        commandhandlers = [
            CommandHandler(
                pos_commands + angrypos_commands + neg_commands + meh_commands,
                self.change_karma
            ),
            CommandHandler(["karma", "getkarma"], self.getkarma),
        ]
        super().__init__(logger, commandhandlers, table, mediafolder="./media")

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

    def change_karma(self, update: Update, context: CallbackContext) -> None:
        """
        Add karma to user by replying to a message.
        """
        if update.message.reply_to_message:
            user = update.message.reply_to_message.from_user
            dbuser = get_user(self.table, user.id, update.message.chat.id)
            command = update.message.text.split(" ", 1)[0][1:]
            if "@" in command:
                # command may be `somecommand@botname``
                command = command.split("@")[0]
            # Self
            if user == update.effective_user:
                if command in pos_commands + angrypos_commands:
                    reply = "Humble bragging, amarite?"
                    log = "{} wants to pos themselves!".format(user.first_name)
                elif command in neg_commands:
                    reply = "Don't be so harsh on yourself."
                    log = "{} wants to neg themselves!".format(user.first_name)
                elif command in meh_commands:
                    reply = "Sooo... Nothing?"
                    log = "{} doesn't know what to do with their karma!".format(user.first_name)
                else:
                    reply="I deadass don't know how to respond"
                    log = "Command {} couldn't be interpreted"
                update.message.reply_text(reply)
                self.logger.info(log)

            # To a reply
            else:
                if command in pos_commands:
                    operator = +1
                    resp = "+1"
                elif command in angrypos_commands:
                    operator = +1
                    resp = "Angry +1"
                elif command in neg_commands:
                    operator = -1
                    resp = "-1"
                elif command in meh_commands:
                    operator = 0
                    resp = "Meh"
                else:
                    operator = 0
                    resp = "Eeh, programmer mistake, what was that?"
                dbuser.karma += operator
                update.message.reply_to_message.reply_text(
                    "{} for {} ({} points).".format(resp, user.first_name, dbuser.karma)
                )

                # Special, if needed
                if command in angrypos_commands:
                    with open(self._media("angrypos.jpg"), "rb") as file:
                        update.message.reply_photo(photo=file, caption="Now get tf outta here.")

                self.logger.info("{} gets a {}!".format(user.first_name, resp))

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
            dbuser = get_user(self.table, user.id, update.message.chat.id)
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

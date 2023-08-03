"""
Karma module is used to handle karma in groupchats.
"""
from peewee import fn
from telegram import Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, CommandHandler


from ..base import admin_only, Base, command_enabled
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
                pos_commands + angrypos_commands + neg_commands + meh_commands, self.change_karma
            ),
            CommandHandler(["karma", "getkarma", "globalkarma"], self.getkarma),
            CommandHandler(["setkarma"], self.setkarma),
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

        return {user.userid: [user.userfirstname, user.karma] for user in users if not user.optouts}

    def _get_global_karma(self):
        query = (
            self.table.select(
                self.table.userid,
                self.table.userfirstname,
                self.table.optout,
                fn.SUM(self.table.karma).alias("karma"),
            )
            .group_by(self.table.userid)
            .order_by(fn.SUM(self.table.karma).desc())
        )
        return {user.userid: [user.userfirstname, user.karma] for user in query if not user.optouts}

    @command_enabled(default=True)
    def change_karma(self, update: Update, context: CallbackContext) -> None:
        """
        Add karma to user by replying to a message.
        """
        if update.message.reply_to_message:
            user = update.message.reply_to_message.from_user
            dbuser = get_user(self.table, user.id, update.message.chat.id)

            # GDPR
            if not dbuser:
                return

            command = update.message.text.split(" ", 1)[0][1:]
            if "@" in command:
                # command may be `somecommand@botname``
                command = command.split("@")[0]
            # Self
            if user == update.effective_user:
                if command in pos_commands + angrypos_commands:
                    reply = "Humble bragging, amarite?"
                    log = f"{user.first_name} wants to pos themselves!"
                elif command in neg_commands:
                    reply = "Don't be so harsh on yourself."
                    log = f"{user.first_name} wants to neg themselves!"
                else:
                    reply = "Sooo... Nothing?"
                    log = f"{user.first_name} doesn't know what to do with their karma!"
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
                else:
                    operator = 0
                    resp = "Meh"
                dbuser.karma += operator
                update.message.reply_to_message.reply_text(
                    f"{resp} for {user.first_name} ({dbuser.karma} points)."
                )

                # Special, if needed
                if command in angrypos_commands:
                    with open(self._media("angrypos.jpg"), "rb") as file:
                        update.message.reply_photo(photo=file, caption="Now get tf outta here.")

                self.logger.info(f"{user.first_name} gets a {resp}!")

            dbuser.userfirstname = user.first_name
            dbuser.save()
        else:
            update.message.reply_text("You must respond to a message to give karma.")

    @command_enabled(default=True)
    def getkarma(self, update: Update, context: CallbackContext) -> None:
        """
        Give the (global) karma score for a user by replying, or karma scores from a chat.
        """
        global_request = "global" in update.message.text

        if update.message.reply_to_message:
            user = update.message.reply_to_message.from_user

            if global_request:
                dbuser = (
                    self.table.select(
                        self.table.userid,
                        self.table.userfirstname,
                        self.table.optout,
                        fn.SUM(self.table.karma).alias("karma"),
                    )
                    .where(self.table.userid == user.id)
                    .get_or_none()
                )
            else:
                dbuser = get_user(self.table, user.id, update.message.chat.id)

            # GDPR and failsafe
            if not dbuser or dbuser.optout or not dbuser.karma:
                update.message.reply_text(f"User not found.")
                return

            dbuser.userfirstname = user.first_name
            dbuser.save()

            update.message.reply_text(
                f"{dbuser.userfirstname} has {dbuser.karma} {'global ' if global_request else ''}points."
            )
            self.logger.info(
                f"{dbuser.userfirstname} has {dbuser.karma} {'global ' if global_request else ''}karma!"
            )

        else:
            try:
                _, num_people = update.message.text.split(" ", 1)
                num_people = int(num_people)
                if num_people < 1:
                    num_people = 10
            except ValueError:
                num_people = 10

            if global_request:
                karmas = self._get_global_karma()
            else:
                karmas = self._get_karma(update.message.chat.id)
            num_people = min(len(karmas), num_people)

            all_people = []
            for i, (_, data) in enumerate(karmas.items()):
                if i < num_people:
                    username, karma = data
                    if not username:
                        username = "<please trigger karma action for name>"
                    if karma != 0:
                        all_people.append(
                            f"{i + 1}. {username}: {karma} {'global ' if global_request else ''}points."
                        )
                else:
                    break

            if all_people:
                update.message.reply_text("\n".join(all_people))
            else:
                update.message.reply_text(f"No {'global ' if global_request else ''}karma so far!")
            self.logger.info(
                f"{update.effective_user.first_name} wants to know the {'global ' if global_request else ''}karmas!"
            )

    @admin_only
    @command_enabled(default=True)
    def setkarma(self, update: Update, context: CallbackContext) -> None:
        """
        Set karma of someone.
        """
        if update.message.reply_to_message:
            user = update.message.reply_to_message.from_user
            dbuser = get_user(self.table, user.id, update.message.chat.id)

            # GDPR
            if not dbuser:
                return

            try:
                _, qt = update.message.text.split(" ")
                qt = int(qt)
            except ValueError:
                return
            dbuser.karma = qt
            dbuser.save()
            self.logger.info(
                f"{update.effective_user.first_name} changed karma of {user.first_name}!"
            )
            try:
                update.message.delete()
            except BadRequest:
                return
        else:
            return

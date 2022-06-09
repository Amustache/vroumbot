"""
Basic Telegram information and administration.
"""
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


from .base import admin_only, Base, command_enabled


class Special(Base):
    """
    Basic Telegram information and administration.
    """

    def __init__(self, logger=None):
        commandhandlers = [
            CommandHandler(["userid", "id"], self.userid),
            CommandHandler(["chatid", "here"], self.chatid),
            CommandHandler(["messageid", "this", "that"], self.messageid),
        ]
        super().__init__(logger, commandhandlers)

    def userid(self, update: Update, context: CallbackContext) -> None:
        """
        Get current userid or replied message's userid.
        """
        if update.message.reply_to_message:
            user = update.message.reply_to_message.from_user
            update.message.reply_text(user.id)
        else:
            user = update.effective_user
            update.message.reply_text(user.id)

        self.logger.info("{} wants their ID! It is {}.".format(user.first_name, user.id))

    @command_enabled
    def chatid(self, update: Update, context: CallbackContext) -> None:
        """
        Get current chatid.
        """
        update.message.reply_text(update.message.chat.id)

        self.logger.info(
            "{} wants the chat ID! It is {}.".format(
                update.effective_user.first_name, update.message.chat.id
            )
        )

    @command_enabled
    def messageid(self, update: Update, context: CallbackContext) -> None:
        """
        Get replied message's messageid.
        """
        if update.message.reply_to_message:
            update.message.reply_text(
                "{} in {}".format(
                    update.message.reply_to_message.message_id, update.message.chat.id
                )
            )

            self.logger.info(
                "{} wants the message ID! It is {} in {}.".format(
                    update.effective_user.first_name,
                    update.message.message_id,
                    update.message.chat.id,
                )
            )

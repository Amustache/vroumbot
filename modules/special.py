"""
Basic Telegram information and administration.
"""
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


from .base import Base, command_enabled


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

    @command_enabled(default=True)
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

        self.logger.info(f"{user.first_name} wants their ID! It is {user.id}.")

    @command_enabled(default=True)
    def chatid(self, update: Update, context: CallbackContext) -> None:
        """
        Get current chatid.
        """
        update.message.reply_text(update.message.chat.id)

        self.logger.info(
            f"{update.effective_user.first_name} wants the chat ID! It is {update.message.chat.id}."
        )

    @command_enabled(default=True)
    def messageid(self, update: Update, context: CallbackContext) -> None:
        """
        Get replied message's messageid.
        """
        if update.message.reply_to_message:
            update.message.reply_text(
                f"{update.message.reply_to_message.message_id} in {update.message.chat.id}"
            )

            self.logger.info(
                f"{update.effective_user.first_name} wants the message ID! It is {update.message.message_id} in {update.message.chat.id}."
            )

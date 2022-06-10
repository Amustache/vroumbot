"""
Admin commands.
"""
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


from .base import admin_only, Base


def get_command_for_chat(table, commandname, chatid):
    """
    Return the user from the database.
    :param table: peewee.Model.
    :param commandname: Name of the command.
    :param chatid: Telegram chatid.
    :return: Model: ChatCommand
    """
    chatcommand, _ = table.get_or_create(commandname=commandname, chatid=chatid)

    return chatcommand


def get_command_from_alias(alias, dispatcher):
    for handler in dispatcher.handlers[0]:
        if alias in handler.command:
            return handler.callback.__name__
    return None


class Admin(Base):
    """
    Admin commands.
    """

    def __init__(self, logger=None, table=None):
        self.dispatcher = None
        commandhandlers = [
            CommandHandler(["enablecommand", "disablecommand"], self.enablecommand),
            CommandHandler(["enablemodule", "disablemodule"], self.enablemodule),
            CommandHandler("amiadmin", self.amiadmin),
        ]
        super().__init__(logger, commandhandlers, table)

    def add_dispatcher(self, dispatcher):
        self.dispatcher = dispatcher
        return self

    @admin_only
    def amiadmin(self, update: Update, context: CallbackContext) -> None:
        """
        Check if one is admin. This is mainly for testing purposes.
        """
        update.message.reply_text("Yes you are (:.")

    @admin_only
    def enablecommand(self, update: Update, context: CallbackContext) -> None:
        try:
            _, commandname = update.message.text.split(" ", 1)
        except ValueError:
            return

        commandname = get_command_from_alias(commandname, self.dispatcher)
        if not commandname:
            update.message.reply_text("This command does not exist.")
            return

        chatcommand = get_command_for_chat(
            self.table, commandname=commandname, chatid=update.message.chat.id
        )

        chatcommand.enabled = not chatcommand.enabled
        chatcommand.save()

        update.message.reply_text(
            "Command {} is now {}abled".format(commandname, "en" if chatcommand.enabled else "dis")
        )

    @admin_only
    def enablemodule(self, update: Update, context: CallbackContext) -> None:
        pass

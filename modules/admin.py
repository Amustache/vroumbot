"""
Module that contains admin commands.
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
    if alias[0] == "/":
        alias = alias[1:]

    for handler in dispatcher.handlers[0]:
        try:
            if alias in handler.command:
                return handler.callback.__name__
        except AttributeError:
            continue
    return None


class Admin(Base):
    """
    Admin commands.
    """

    def __init__(self, logger=None, table=None, dispatcher=None):
        self.dispatcher = None
        commandhandlers = [
            CommandHandler(
                ["enablecommand", "disablecommand", "enable", "disable"], self.enablecommand
            ),
            CommandHandler(["enablemodule", "disablemodule"], self.enablemodule),
            CommandHandler("amiadmin", self.amiadmin),
            CommandHandler(["listcommands", "listenabled", "listdisabled"], self.listenabled),
        ]
        super().__init__(
            logger=logger, commandhandlers=commandhandlers, table=table, dispatcher=dispatcher
        )

    @admin_only
    def amiadmin(self, update: Update, context: CallbackContext) -> None:
        """
        Check if one is admin. This is mainly for testing purposes.
        """
        update.message.reply_text("Yes you are (:.")

    @admin_only
    def enablecommand(self, update: Update, context: CallbackContext) -> None:
        """
        Enable or disable a command.
        """
        try:
            choice, commandname = update.message.text.split(" ", 1)
        except ValueError:
            return

        commandname = get_command_from_alias(commandname, self.dispatcher)
        if not commandname:
            update.message.reply_text("This command does not exist.")
            return

        chatcommand = get_command_for_chat(
            self.table, commandname=commandname, chatid=update.message.chat.id
        )

        if "en" in choice:
            chatcommand.enabled = 1
        elif "dis" in choice:
            chatcommand.enabled = 0
        else:
            return

        chatcommand.save()

        update.message.reply_text(
            "Command {} is now {}abled".format(commandname, "en" if chatcommand.enabled else "dis")
        )

    @admin_only
    def enablemodule(self, update: Update, context: CallbackContext) -> None:
        pass

    def listenabled(self, update: Update, context: CallbackContext) -> None:
        chat_id = update.message.chat.id
        dbcommands = (
            self.table.select().where(self.table.chatid == chat_id).order_by(self.table.fun.desc())
        )
        commands = [
            f"– {command.enabled} {command.commandname} (Last usage: {command.lastusage})"
            for command in dbcommands
        ]

        print(commands)

        # if "en" in update.message.text:
        # elif "dis" in update.message.text:
        # else:

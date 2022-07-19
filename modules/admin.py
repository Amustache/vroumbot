"""
Module that contains admin commands.
"""
import datetime
import json
import random


from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
import requests


from secret import ADMIN_ID, GITHUB_REPO, GITHUB_TOKEN, GITHUB_USERNAME


from .base import admin_only, Base, command_enabled
from .community.helpers import naturaltime


CANNOT_DISABLE = [
    "enablecommand",
    "enablemodule",
    "amiadmin",
    "start",
    "help_command",
    "contribute",
    "feedback",
    "feedbacks",
    "reset_from_history",
    "optout",
    "gdpr",
]


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
                ["enablecommand", "disablecommand", "enable", "disable", "activate", "deactivate"],
                self.enablecommand,
            ),
            CommandHandler(["enablemodule", "disablemodule"], self.enablemodule),
            CommandHandler("amiadmin", self.amiadmin),
            CommandHandler(["listcommands", "listenabled", "listdisabled"], self.listenabled),
            CommandHandler("reboot", self.reboot),
        ]
        super().__init__(
            logger=logger, commandhandlers=commandhandlers, table=table, dispatcher=dispatcher
        )

    @admin_only
    def amiadmin(self, update: Update, context: CallbackContext) -> None:
        """
        Check if one is admin. This is mainly for testing purposes.
        """
        if update.message.chat.type == "private":
            update.message.reply_text("You're in private, silly~")
            return

        update.message.reply_text("Yes you are (:.")

    @admin_only
    def enablecommand(self, update: Update, context: CallbackContext) -> None:
        """
        Enable or disable a command.
        """
        if update.message.chat.type == "private":
            update.message.reply_text("You're in private, silly~")
            return

        try:
            choice, commandname = update.message.text.split(" ", 1)
        except ValueError:
            return

        commandname = get_command_from_alias(commandname, self.dispatcher)
        if not commandname:
            update.message.reply_text("This command does not exist.")
            return

        if commandname in CANNOT_DISABLE:
            if commandname == "enablecommand" and random.randint(1, 6) == 6:
                update.message.reply_text(
                    "Oh no! You found a loophole and broke the bot!\n...\nNah just kidding."
                )

            update.message.reply_text("This command cannot be disabled.")
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

    @command_enabled(default=True)
    def listenabled(self, update: Update, context: CallbackContext) -> None:
        if update.message.chat.type == "private":
            update.message.reply_text("You're in private, silly~")
            return

        chat_id = update.message.chat.id
        dbcommands = (
            self.table.select().where(self.table.chatid == chat_id).order_by(self.table.commandname)
        )

        text = "List of commands explicitly enabled by admin:\n"
        text += "\n".join(
            [f"– ✅ {command.commandname}" for command in dbcommands if command.enabled]
        )
        text += "\n\n"

        text += "List of commands explicitly disabled by admin:\n"
        text += "\n".join(
            [
                f"– ❌ {command.commandname} (Last attempt: {naturaltime(datetime.datetime.now() - command.lastusage, past=True)})"
                for command in dbcommands
                if not command.enabled
            ]
        )
        text += "\n\n"

        text += "For a list of by default enabled/disabled commands, please refer to: "
        text += "https://github.com/Amustache/vroumbot/wiki/Commands"

        update.message.reply_text(text, disable_web_page_preview=True)

    @admin_only
    def reboot(self, update: Update, context: CallbackContext) -> None:
        if update.message.chat.id != ADMIN_ID:
            return

        if len(context.args) != 1:
            update.message.reply_text("Workflow name needed.")
            return

        headers = {
            "Accept": "application/vnd.github+json",
            "Authorization": f"token {GITHUB_TOKEN}",
        }
        data = {
            "event_type": context.args[0],
        }
        requests.post(
            f"https://api.github.com/repos/{GITHUB_USERNAME}/{GITHUB_REPO}/dispatches",
            headers=headers,
            data=json.dumps(data),
        )

        update.message.reply_text("🥱 Bot is now rebooting...")

"""
Base class to add new features in the bot.
"""
from functools import wraps
import datetime
import os


from databases import ChatCommand


def admin_only(func):
    @wraps(func)
    def wrapped(self, update, context, *args, **kwargs):
        is_admin = update.effective_user in [
            chatmember.user
            for chatmember in context.bot.get_chat_administrators(update.message.chat.id)
        ]

        if not is_admin:
            context.bot.sendMessage(
                chat_id=update.message.chat.id, text="This command is restricted to admins only."
            )
            return
        return func(self, update, context, *args, **kwargs)

    return wrapped


# def module_enabled(func):
#     @wraps(func)
#     def wrapped(self, update, context, *args, **kwargs):
#         chatmodule = ChatModule.get_or_none(
#             chatid=update.message.chat.id, commandname=func.__name__
#         )
#
#         if chatmodule and not chatmodule.enabled:
#             context.bot.sendMessage(
#                 chat_id=update.message.chat.id,
#                 text="This command is in a module deactivated in that chat.",
#             )
#             return
#         return func(self, update, context, *args, **kwargs)
#
#     return wrapped


def command_enabled(default=True):
    def command_enabled_inner(func):
        @wraps(func)
        def wrapped(self, update, context, *args, **kwargs):
            chatcommand, created = ChatCommand.get_or_create(
                chatid=update.message.chat.id, commandname=func.__name__
            )

            enabled = chatcommand.enabled

            if created:
                chatcommand.enabled = 1 if default else 0
                chatcommand.lastusage = datetime.datetime.now()
                chatcommand.save()
                enabled = default

            if chatcommand and not enabled:
                if created or datetime.datetime.now() > chatcommand.lastusage + datetime.timedelta(
                    hours=6
                ):
                    context.bot.sendMessage(
                        chat_id=update.message.chat.id,
                        text="This command is deactivated in that chat.",
                    )
                chatcommand.lastusage = datetime.datetime.now()
                chatcommand.save()
                return
            return func(self, update, context, *args, **kwargs)

        return wrapped

    return command_enabled_inner


class Base:
    """
    Base class to add new features in the bot.
    """

    def __init__(
        self, logger=None, commandhandlers=None, table=None, mediafolder=None, dispatcher=None
    ):
        """
        :param logger: logging.getLogger, when using a logger.
        :param commandhandlers: [telegram.ext.CommandHandler], for command handling.
        :param table: peewee.ModelBase, when using a table in the bot's database.
        """
        self.logger = logger
        self.commandhandlers = commandhandlers
        self.table = table
        self.mediafolder = mediafolder
        self.dispatcher = dispatcher

    def _media(self, filename=""):
        if self.mediafolder:
            return os.path.join(self.mediafolder, filename)

    def add_commands(self, dispatcher):
        """
        Add all self.commandhandlers to the provided dispatcher.
        :param dispatcher: telegram.ext.Dispatcher
        """
        for commandhandler in self.commandhandlers:
            dispatcher.add_handler(commandhandler)

    def get_commands(self):
        """
        :return: Aliases and commands in text format.
        """
        commands = ""
        for handler in self.commandhandlers:
            try:
                commands += f"- {', '.join(handler.command)} => {handler.callback.__name__};\n"
            except:
                continue

    def get_commands_botfather(self):
        """
        :return: Aliases and commands but formatted for botfather.
        """
        commands = ""
        for handler in self.commandhandlers:
            try:
                commands += [
                    f"{command} - {handler.callback.__name__}\n" for command in handler.command
                ]
            except:
                continue

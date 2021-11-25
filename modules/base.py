"""
Base class to add new features in the bot.
"""
import os


class Base:
    """
    Base class to add new features in the bot.
    """

    def __init__(self, logger=None, commandhandlers=None, table=None, mediafolder=None):
        """
        :param logger: logging.getLogger, when using a logger.
        :param commandhandlers: [telegram.ext.CommandHandler], for command handling.
        :param table: peewee.ModelBase, when using a table in the bot's database.
        """
        self.logger = logger
        self.commandhandlers = commandhandlers
        self.table = table
        self.mediafolder = mediafolder

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
                commands += "- {} => {};\n".format(
                    ", ".join(handler.command), handler.callback.__name__
                )
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
                    "{} - {}\n".format(command, handler.callback.__name__)
                    for command in handler.command
                ]
            except:
                continue

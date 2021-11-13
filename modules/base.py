class Base:
    def __init__(self, logger=None, commandhandlers=None):
        """
        :param logger: logging.getLogger
        :param commandhandlers: [telegram.ext.CommandHandler]
        """
        self.logger = logger
        self.commandhandlers = commandhandlers

    def add_commands_to_dispatcher(self, dispatcher):
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
                commands += "- {} => {};\n".format(", ".join(handler.command), handler.callback.__name__)
            except:
                continue

    def get_commands_botfather(self):
        """
        :return: Aliases and commands but formatted for botfather.
        """
        commands = ""
        for handler in self.commandhandlers:
            try:
                commands += ["{} - {}\n".format(command, handler.callback.__name__) for command in handler.command]
            except:
                continue

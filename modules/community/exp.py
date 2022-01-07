from telegram import Update
from telegram.ext import CallbackContext, CommandHandler


from ..base import Base
from .helpers import get_user


class Exp(Base):
    def __init__(self, logger=None, table=None):
        commandhandlers = []
        super().__init__(logger, commandhandlers, table, mediafolder="./media/exp")

    def _get_current_level(self, nummessages, karma):
        

    def _needed_exp(self, level, karma):
        if level == 1:
            return 1

        return int((level ** 3.14) * (1 - (karma / ((level - 1) ** 3.14))))

    def _get_next_level_needed_exp(self, nummessages, karma):
        current_level = self._get_current_level(nummessages, karma)

        return self._needed_exp(current_level + 1, karma)










    def _get_level(self, chatid):
        numbermessages = self._get_numbermessages(chatid)

        return {user.userid: [user.userfirstname, user.numbermessages] for user in users}

# TODO
# state (start or stop)(if admin?)
# reset/import chat (with or without file)

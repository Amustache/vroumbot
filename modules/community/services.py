"""
Services are external things that can help to organize, for instance.
"""
from datetime import datetime, timedelta


from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
import requests


from ..base import Base, command_enabled


class Services(Base):
    """
    Services are external things that can help to organize, for instance.
    """

    def __init__(self, logger=None, table=None):
        commandhandlers = [
            CommandHandler(["w2m", "when2meet"], self.w2m),
        ]
        super().__init__(logger, commandhandlers, table, mediafolder="./media")

    @command_enabled(default=True)
    def w2m(self, update: Update, context: CallbackContext) -> None:
        """
        For important meetings.
        """
        try:
            _, start, end = update.message.text.split()
            start = int(start)
            end = int(end)
        except ValueError:
            start = 1
            end = 7

        base_url = "https://whenufree.io/"
        today = datetime.today()
        dates = [
            (today + timedelta(i)).strftime("%Y-%m-%dT10:00:00.000Z") for i in range(start, end)
        ]

        payload = {
            "eventName": "Vroum le meeting en fait",
            "dates": dates,
            "times": {"start": {"hour": 8, "block": 0}, "end": {"hour": 20, "block": 0}},
            "timezone": "(UTC+0) GMT London",
        }
        response = requests.post(f"{base_url}api/events/create", json=payload)
        if response.status_code == 200:
            result_url = f"{base_url}{response.json()['url']}"
            update.message.reply_text(f"Fill in the when2meet!\n{result_url}")
        else:
            return

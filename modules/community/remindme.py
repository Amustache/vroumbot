"""
Reminders and alarms within a groupchat.
"""
import datetime


from telegram import Update
from telegram.constants import CHAT_SUPERGROUP, PARSEMODE_HTML
from telegram.ext import CallbackContext, CommandHandler
import dateparser


from modules.base import Base


def naturaltime(delta):
    """
    Return a nice phrasing for the remaining time.
    :param delta: datetime.timedelta
    :return: Phrasing: String.
    """
    time_strings = {
        "now": "now",
        "second": ("in a second", "in {} seconds"),
        "minute": ("in a minute", "in {} minutes"),
        "hour": ("in an hour", "in {} hours"),
        "day": ("in a day", "in {} days"),
        "week": ("in a week", "in {} weeks"),
        "month": ("in a month", "in {} months"),
        "year": ("in a year", "in {} years"),
    }

    if delta.days != 0:
        if delta.days < 7:
            if delta.days == 1:
                return time_strings["day"][0]
            else:
                return time_strings["day"][1].format(delta.days)
        elif delta.days // 7 < 4:
            if delta.days // 7 == 1:
                return time_strings["week"][0]
            else:
                return time_strings["week"][1].format(delta.days // 7)
        elif delta.days // 7 // 4 < 12:
            if delta.days // 7 // 4 == 1:
                return time_strings["month"][0]
            else:
                return time_strings["month"][1].format(delta.days // 7 // 4)
        else:
            if delta.days // 7 // 4 // 12 == 1:
                return time_strings["year"][0]
            else:
                return time_strings["year"][1].format(delta.days // 7 // 4 // 12)
    else:
        if delta.seconds == 0:
            return time_strings["now"]
        elif delta.seconds < 60:
            if delta.seconds == 1:
                return time_strings["second"][0]
            else:
                return time_strings["second"][1].format(delta.seconds)
        elif delta.seconds // 60 < 60:
            if delta.seconds // 60 == 1:
                return time_strings["minute"][0]
            else:
                return time_strings["minute"][1].format(delta.seconds // 60)
        else:
            if delta.seconds // 60 // 60 == 1:
                return time_strings["hour"][0]
            else:
                return time_strings["hour"][1].format(delta.seconds // 60 // 60)


class RemindMe(Base):
    """
    Reminders and alarms within a groupchat.
    """

    def __init__(self, logger=None):
        commandhandlers = [
            CommandHandler(["remindme", "remind_me", "set", "alarm"], self.remindme),
            CommandHandler(
                [
                    "listremindme",
                    "listjobs",
                    "listalarms",
                ],
                self.allremindme,
            ),
        ]
        super().__init__(logger, commandhandlers)

    # Borrowed from https://github.com/django/django/blob/main/django/contrib/humanize/templatetags/humanize.py#L169, but worse

    def alarm(self, context: CallbackContext) -> None:
        """
        Helper function to send the actual alarm message.
        """
        job = context.job
        context.bot.send_message(
            job.context["chat_id"], text="Reminder!", reply_to_message_id=job.context["message_id"]
        )

    def remindme(self, update: Update, context: CallbackContext) -> None:
        """
        Create a remindme with a deadline in argument, in reply to a message.
        """
        chat_id = update.message.chat_id
        message_id = update.message.message_id

        try:
            _, message = update.message.text.split(" ", 1)
            print(message)
            interpreted = dateparser.parse(message)
            if not interpreted:
                update.message.reply_text("I didn't understand, sorry...")
                return

            delta = (interpreted - datetime.datetime.now()) + datetime.timedelta(seconds=1)
            if delta.total_seconds() < 0:
                if delta.total_seconds() < -1:
                    update.message.reply_text("Sorry we can not go back to future!")
                else:
                    update.message.reply_text("Okay, that may be a bit too close anyway.")
                return

            context.job_queue.run_once(
                self.alarm,
                delta.total_seconds(),
                context={"chat_id": chat_id, "message_id": message_id},
                name="{}_{}".format(chat_id, message_id),
            )

            update.message.reply_text(
                "I will remind you this {} ({})!".format(
                    naturaltime(delta), str(delta).split(".", maxsplit=1)[0]
                )
            )

            self.logger.info("{} set an alarm!".format(update.effective_user.first_name))
        except (IndexError, ValueError):
            update.message.reply_text("It seems like you used that command wrong. (:.")

    def allremindme(self, update: Update, context: CallbackContext) -> None:
        """
        Lists all remindme from a specific chat.
        """
        jobs = context.job_queue.jobs()
        if update.message.chat.type == CHAT_SUPERGROUP:
            liste = [
                "- #<a href='https://t.me/c/{}/{}'>{}</a>: {}.".format(
                    str(job.context["chat_id"])[4:],
                    job.context["message_id"],
                    job.context["message_id"],
                    str(job.next_t).split(".", maxsplit=1)[0],
                )
                for job in jobs
                if job.context["chat_id"] == update.message.chat_id
            ]
        else:
            liste = [
                "- #{}: {}.".format(i, str(job.next_t).split(".", maxsplit=1)[0])
                for i, job in enumerate(jobs)
                if job.context["chat_id"] == update.message.chat_id
            ]
        update.message.reply_text(
            "List of reminders:\n{}".format("\n".join(liste)), parse_mode=PARSEMODE_HTML
        )

        self.logger.info("{} wants all alarm!".format(update.effective_user.first_name))

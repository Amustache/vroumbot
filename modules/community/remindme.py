"""
Reminders and alarms within a groupchat.
"""
import datetime


from telegram import Update
from telegram.constants import CHAT_SUPERGROUP, PARSEMODE_HTML
from telegram.ext import CallbackContext, CommandHandler
import dateparser


from databases import start_jobs_in_database


from ..base import Base, command_enabled
from .helpers import alarm, naturaltime


class RemindMe(Base):
    """
    Reminders and alarms within a groupchat.
    """

    def __init__(self, logger=None, table=None, dispatcher=None):
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
        super().__init__(
            logger=logger, commandhandlers=commandhandlers, table=table, dispatcher=dispatcher
        )

        start_jobs_in_database(self.dispatcher, alarm)

    # Borrowed from https://github.com/django/django/blob/main/django/contrib/humanize/templatetags/humanize.py#L169, but worse

    @command_enabled(default=True)
    def remindme(self, update: Update, context: CallbackContext) -> None:
        """
        Create a remindme with a deadline in argument, in reply to a message.
        """
        chat_id = update.message.chat_id
        message_id = update.message.message_id

        try:
            _, message = update.message.text.split(" ", 1)
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
                alarm,
                delta.total_seconds(),
                context={"chat_id": chat_id, "message_id": message_id},
                name=f"{chat_id}_{message_id}",
            )

            # Add job to database in case of crash
            self.table.create(
                chatid=chat_id, messageid=message_id, deadline=interpreted, fun=alarm.__name__
            )

            update.message.reply_text(
                f"I will remind you this {naturaltime(delta)} ({str(delta).split('.', maxsplit=1)[0]})!"
            )

            self.logger.info(f"{update.effective_user.first_name} sets an alarm!")
        except (IndexError, ValueError):
            update.message.reply_text("It seems like you used that command wrong.")

    @command_enabled(default=True)
    def allremindme(self, update: Update, context: CallbackContext) -> None:
        """
        Lists all remindme from a specific chat.
        """
        jobs = context.job_queue.jobs()
        if update.message.chat.type == CHAT_SUPERGROUP:
            liste = [
                f"- #<a href='https://t.me/c/{str(job.context['chat_id'])[4:]}/{job.context['message_id']}'>{job.context['message_id']}</a>: {str(job.next_t).split('.', maxsplit=1)[0]}."
                for job in jobs
                if job.context["chat_id"] == update.message.chat_id
            ]
        else:
            liste = [
                f"- #{i}: {str(job.next_t).split('.', maxsplit=1)[0]}."
                for i, job in enumerate(jobs)
                if job.context["chat_id"] == update.message.chat_id
            ]
        update.message.reply_text(
            "List of reminders:\n{}".format("\n".join(liste)), parse_mode=PARSEMODE_HTML
        )

        self.logger.info(f"{update.effective_user.first_name} wants all alarm!")

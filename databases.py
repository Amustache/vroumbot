import datetime


from peewee import BigIntegerField, CharField, DateTimeField, IntegerField, Model, SqliteDatabase


# Database
main_db = SqliteDatabase("./databases/main.db")


class User(Model):
    """
    User model to access the database.
    """

    userid = BigIntegerField()
    userfirstname = CharField(null=True)
    chatid = BigIntegerField()
    karma = IntegerField(default=0)
    num_messages = IntegerField(default=0)
    level = IntegerField(default=0)

    class Meta:
        """
        Basically which database.
        """

        database = main_db


class ChatCommand(Model):
    """
    Chat command model to access the database.
    """

    chatid = BigIntegerField()
    commandname = CharField()
    enabled = IntegerField(default=1)
    lastusage = DateTimeField(default=datetime.datetime.now())

    class Meta:
        """
        Basically which database.
        """

        database = main_db


class ChatJob(Model):
    """
    Chat command model to access the database.
    """

    chatid = BigIntegerField()
    messageid = BigIntegerField()
    deadline = DateTimeField()

    class Meta:
        """
        Basically which database.
        """

        database = main_db


for job in ChatJob.select():
    delta = (job.deadline - datetime.datetime.now()) + datetime.timedelta(seconds=1)
    if delta.total_seconds() < 1:
        job.delete_instance()
    else:
        dispatcher.job_queue.run_once(
            None,
            delta.total_seconds(),
            context={"chat_id": job.chatid, "message_id": job.messageid},
            name="{}_{}".format(job.chatid, job.messageid),
        )

# class ChatModule(Model):
#     """
#     Chat command model to access the database.
#     """
#
#     chatid = BigIntegerField()
#     modulename = CharField()
#     enabled = IntegerField(default=1)
#
#     class Meta:
#         """
#         Basically which database.
#         """
#
#         database = main_db


main_db.connect()
main_db.create_tables([User, ChatCommand])

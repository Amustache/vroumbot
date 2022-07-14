import datetime


from peewee import BigIntegerField, CharField, DateTimeField, IntegerField, Model, SqliteDatabase


main_db = SqliteDatabase("./databases/main.db")


class User(Model):
    """
    User model to access the database.
    """

    userid = BigIntegerField()
    chatid = BigIntegerField()
    optout = IntegerField(default=0)
    userfirstname = CharField(null=True)
    karma = IntegerField(default=0)
    num_messages = IntegerField(default=0)
    level = IntegerField(default=0)

    class Meta:
        """
        Basically which database.
        """

        database = main_db


class GDPR(Model):
    """
    Opt-out.
    """

    userid = BigIntegerField()

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
    fun = CharField()
    deadline = DateTimeField()

    class Meta:
        """
        Basically which database.
        """

        database = main_db


def start_jobs_in_database(dispatcher, fun):
    for job in ChatJob.select().where(ChatJob.fun == fun.__name__):
        delta = (job.deadline - datetime.datetime.now()) + datetime.timedelta(seconds=1)
        if delta.total_seconds() < 1:
            job.delete_instance()
        else:
            dispatcher.job_queue.run_once(
                fun,
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
main_db.create_tables([User, GDPR, ChatCommand, ChatJob])

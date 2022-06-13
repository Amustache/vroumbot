from peewee import BigIntegerField, CharField, IntegerField, Model, SqliteDatabase


my_db = SqliteDatabase("./databases/main.db")


class ChatCommand(Model):
    """
    Chat command model to access the database.
    """

    chatid = BigIntegerField()
    commandname = CharField()
    enabled = IntegerField(default=1)

    class Meta:
        """
        Basically which database.
        """

        database = my_db


# Add migration here
my_db.create_tables([ChatCommand])

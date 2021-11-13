from peewee import *
from playhouse.migrate import *


my_db = SqliteDatabase("main.db")
migrator = SqliteMigrator(my_db)

# Add migration here
userfirstname = CharField(null=True)

migrate(
    migrator.add_column("User", "userfirstname", userfirstname),
)

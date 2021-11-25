from peewee import CharField, SqliteDatabase
from playhouse.migrate import migrate, SqliteMigrator


my_db = SqliteDatabase("main.db")
migrator = SqliteMigrator(my_db)

# Add migration here
userfirstname = CharField(null=True)

migrate(
    migrator.add_column("User", "userfirstname", userfirstname),
)

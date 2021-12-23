from peewee import IntegerField, SqliteDatabase
from playhouse.migrate import migrate, SqliteMigrator


my_db = SqliteDatabase("./databases/main.db")
migrator = SqliteMigrator(my_db)

# Add migration here
nummessages = IntegerField(null=True)

migrate(
    migrator.add_column("User", "nummessages", nummessages),
)

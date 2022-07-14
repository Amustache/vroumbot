from peewee import IntegerField, SqliteDatabase
from playhouse.migrate import migrate, SqliteMigrator


my_db = SqliteDatabase("./databases/main.db")
migrator = SqliteMigrator(my_db)

# Add migration here
optout = IntegerField(default=0)

migrate(
    migrator.add_column("User", "optout", optout),
)

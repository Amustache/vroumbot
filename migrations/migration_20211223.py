from peewee import IntegerField, SqliteDatabase
from playhouse.migrate import migrate, SqliteMigrator


my_db = SqliteDatabase("./databases/main.db")
migrator = SqliteMigrator(my_db)

# Add migration here
num_messages = IntegerField(default=0)
level = IntegerField(default=0)

migrate(
    migrator.add_column("User", "num_messages", num_messages),
    migrator.add_column("User", "level", level),
)

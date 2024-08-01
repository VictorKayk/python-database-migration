import json
from dotenv import load_dotenv
import os
from database_connection import MysqlConnection
from database_properties import DatabaseProperties
from migration_executor import MigrationExecutor
from migration import Migration, Migration_Column

load_dotenv()

def get_migrations():
    migrations: list[Migration] = []
    with open('migrations.json') as file:
        migrations_from_file = json.load(file)
        for migration_from_file in migrations_from_file:
            columns: Migration_Column = []
            for column in migration_from_file['columns']:
                columns.append(Migration_Column(column['old'], column['new'], column['type']))
            migrations.append(Migration(migration_from_file['old_table'], migration_from_file['new_table'], columns))
    return migrations

def main():
    try:
        old_database = MysqlConnection(DatabaseProperties(os.getenv("OLD_HOST"), os.getenv("OLD_PORT"), os.getenv("OLD_USER"), os.getenv("OLD_PASSWORD"), os.getenv("OLD_DATABASE")))
        new_database = MysqlConnection(DatabaseProperties(os.getenv("NEW_HOST"), os.getenv("NEW_PORT"), os.getenv("NEW_USER"), os.getenv("NEW_PASSWORD"), os.getenv("NEW_DATABASE")))

        migrations = get_migrations()
            
        migration_executor = MigrationExecutor(old_database, new_database, migrations)
        print("Migration started!")
        migration_executor.migrate()
        print("Migration finished!")
    except Exception as e:
        print("An error occurred: ", e)
        exit(1)

if __name__ == '__main__':
    main()

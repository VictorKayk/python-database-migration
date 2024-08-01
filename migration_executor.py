from database_connection import DatabaseConnection
from migration import Migration

class MigrationExecutor:
    def __init__(self, old_database: DatabaseConnection, new_database: DatabaseConnection, migrations: list[Migration]):
        self.old_database = old_database
        self.new_database = new_database
        self.migrations = migrations
        
    def get_dics_from_row(self,     migration: Migration, row):
        dics = {}
        for column in migration.columns:
            if column.type == 'datetime':
                dics[column.new] = row[column.old].strftime('%Y-%m-%d %H:%M:%S')
            else:
                dics[column.new] = row[column.old]
        return dics

    def migrate(self):
        for migration in self.migrations:
            old_data = self.old_database.select_data(migration.old_table)
            
            for _, row in old_data.iterrows():
                dics = self.get_dics_from_row(migration, row)
                self.new_database.insert_data(migration.new_table, list(dics.keys()), dics)
            
            print(f"Migration {migration.old_table} -> {migration.new_table} done! {len(old_data)} rows migrated.") 
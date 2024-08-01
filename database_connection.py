from sqlalchemy import create_engine, text
import pandas as pd
from database_properties import DatabaseProperties

class DatabaseConnection:
    def get_connection(self):
        return self.engine.connect()
    
    def select_data(self, table):
        try:
            connection = self.get_connection()
            return pd.read_sql(f"SELECT * FROM {table}", connection)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            connection.close()
            
    def insert_data(self, table, columns, values):
        try:
            connection = self.get_connection()
            query = text(f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join([':' + str(column) for column in columns])});")
            connection.execute(query, values)
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            connection.close()

class MysqlConnection (DatabaseConnection):
    def __init__(self,  databaseProperty: DatabaseProperties):
        self.engine = create_engine(f'mysql+pymysql://{databaseProperty.user}:{databaseProperty.password}@{databaseProperty.host}:{databaseProperty.port}/{databaseProperty.database}')
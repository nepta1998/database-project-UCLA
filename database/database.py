import sqlite3
from sqlite3 import Error


class Database:
    def __init__(self):
        try:
            self.connection = sqlite3.connect('database.db')
        except Error:
            print(Error)

    def execute_query(self, query, parameters=()):
        cursor = self.connection.cursor()
        result = cursor.execute(query, parameters)
        self.connection.commit()
        return result

    def get_list_events(self):
        query = 'SELECT * FROM Evento'
        database_rows = self.execute_query(query)
        return database_rows

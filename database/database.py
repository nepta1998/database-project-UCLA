import sqlite3
from sqlite3 import Error


def sql_connection():
    try:
        connection = sqlite3.connect('database.db')
        return connection
    except Error:
        print(Error)



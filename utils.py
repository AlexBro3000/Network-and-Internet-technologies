import sqlite3
from models.block_database_model import TableDatabase


def init_database():
    conn = Connect.get_connect()

    TableDatabase.create_tables(conn)
    TableDatabase.fill_out_tables(conn)

    Connect.close_connect(conn)


class Connect:
    @staticmethod
    def get_connect():
        return sqlite3.connect('database.sqlite')

    @staticmethod
    def close_connect(conn):
        conn.close()

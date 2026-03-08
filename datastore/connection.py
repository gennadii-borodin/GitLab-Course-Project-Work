import psycopg2
from psycopg2 import Error
import os


class Connection(object):
    def __init__(self, conf):
        self.config = conf
        self.db_connection = None

    def __enter__(self):
        self.db_connection = self.create_connection()
        return self.db_connection

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value or exc_type or traceback:
            print(exc_value)
            print(exc_type)
            print(traceback)
            self.db_connection.rollback()
        else:
            self.db_connection.commit()
        self.db_connection.close()

    def create_connection(self):
        conn = None
        try:
            conn = psycopg2.connect(
                host=self.config.pg_host,
                port=self.config.pg_port,
                user=self.config.pg_user,
                password=self.config.pg_password,
                database=self.config.pg_database
            )
            return conn
        except Error as e:
            print(e)
        return conn
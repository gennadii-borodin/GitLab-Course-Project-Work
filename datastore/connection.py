import psycopg2
from psycopg2 import Error
import os
from utils.logger import get_logger

logger = get_logger(__name__)


class Connection(object):
    def __init__(self, conf):
        self.config = conf
        self.db_connection = None

    def __enter__(self):
        logger.debug("Opening database connection")
        self.db_connection = self.create_connection()
        return self.db_connection

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value or exc_type or traceback:
            logger.error(f"Database transaction failed: {exc_value}", exc_info=True)
            self.db_connection.rollback()
        else:
            logger.debug("Committing database transaction")
            self.db_connection.commit()
        self.db_connection.close()
        logger.debug("Database connection closed")

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
            logger.info(f"Connected to PostgreSQL database: {self.config.pg_database} on {self.config.pg_host}:{self.config.pg_port}")
            return conn
        except Error as e:
            logger.error(f"Failed to connect to database: {e}")
        return conn

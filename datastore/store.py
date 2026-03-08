import os.path
import json
from psycopg2 import Error
from datastore.connection import Connection
from utils.logger import get_logger

logger = get_logger(__name__)


class Store:

    @staticmethod
    def migrate_db(conf):
        schema_version = Store.check_schema_version(conf)

        file = os.path.join(conf.data_directory, conf.migrations_filename)
        data = None
        with open(file, 'r') as f:
            data = json.load(f)
        if data:
            for m in data["migrations"]:
                if m["version"] > schema_version:
                    Store.execute_migration(m, conf)

    @staticmethod
    def check_schema_version(conf):
        schema_version = 0
        logger.debug("Checking database schema version")
        with Connection(conf) as db_connection:
            try:
                c = db_connection.cursor()
                sql = 'select max(version) from migrations;'
                logger.debug(f"Executing SQL: {sql}")
                c.execute(sql)
                row = c.fetchone()
                if row:
                    schema_version = row[0]
            except Error as err:
                # If migrations table doesn't exist, return 0 to apply all migrations
                if "relation \"migrations\" does not exist" in str(err):
                    logger.info("Migrations table does not exist yet, starting from version 0")
                else:
                    logger.error(f"Failed to check schema version: {err}")
        logger.info(f"Current database schema version: {schema_version}")
        return schema_version

    @staticmethod
    def execute_migration(migration, conf):
        logger.info(f"Applying migration v{migration['version']}: {migration['comment']}")
        with Connection(conf) as db_connection:
            try:
                c = db_connection.cursor()
                sql = migration["sql"]
                logger.debug(f"Migration SQL: {sql}")
                c.execute(sql)
                sql = 'insert into migrations(version, comment, migration_date) values (%s, %s, CURRENT_TIMESTAMP);'
                logger.debug(f"Record migration SQL: {sql}")
                c.execute(sql, (migration["version"], migration["comment"]))
                logger.info(f"Migration v{migration['version']} applied successfully")
            except Error as err:
                logger.error(f"Migration v{migration['version']} failed: {err}")

    @staticmethod
    def import_test_data(conf, table, json_data_file):
        logger.info(f"Importing test data to '{table}' from '{json_data_file}'")
        data = None
        with open(json_data_file, 'r') as f:
            data = json.load(f)
        if data:
            logger.info(f"Found {len(data)} records to import")
            with Connection(conf) as db_connection:
                try:
                    c = db_connection.cursor()
                    for item in data:
                        columns = list(item.keys())
                        values = []
                        for k in columns:
                            values.append(item[k])
                        placeholders = ', '.join(['%s'] * len(columns))
                        cols = ', '.join(columns)
                        sql = f'insert into {table}({cols}) values ({placeholders});'
                        logger.debug(f"Executing SQL: {sql} with values {tuple(values)}")
                        c.execute(sql, tuple(values))
                    logger.info(f"Successfully imported {len(data)} records into '{table}'")
                except Error as err:
                    logger.error(f"Failed to import test data: {err}")


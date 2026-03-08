import os.path
import json
from psycopg2 import Error
from datastore.connection import Connection


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
        with Connection(conf) as db_connection:
            try:
                c = db_connection.cursor()
                sql = 'select max(version) from migrations;'
                row = c.execute(sql).fetchone()
                if row:
                    schema_version = row[0]
            except Error as err:
                print(err)
        print(f'max schema version = {schema_version}')
        return schema_version

    @staticmethod
    def execute_migration(migration, conf):
        with Connection(conf) as db_connection:
            try:
                c = db_connection.cursor()
                sql = migration["sql"]
                print(sql)
                c.execute(sql)
                sql = 'insert into migrations(version, comment, migration_date) values (%s, %s, CURRENT_TIMESTAMP);'
                print(sql)
                c.execute(sql, (migration["version"], migration["comment"]))
            except Error as err:
                print(err)

    @staticmethod
    def import_test_data(conf, table, json_data_file):
        print(f'importing data to {table} from {json_data_file}')
        data = None
        with open(json_data_file, 'r') as f:
            data = json.load(f)
        if data:
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
                        print(sql)
                        c.execute(sql, tuple(values))
                except Error as err:
                    print(err)


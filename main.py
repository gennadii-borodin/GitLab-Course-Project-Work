import os
from bottle import run
from data.config import Config
from datastore.store import Store
import api

if __name__ == '__main__':
    print("Starting up...")

    Config()
    Store.migrate_db(Config.config)

    run(host='localhost', port=Config.config.port)

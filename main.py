import os
from data.config import Config

# Initialize config FIRST before any other imports that might use logger
Config()

from bottle import run
from datastore.store import Store
import api
from utils.logger import setup_logger, get_logger

# Now setup logger with the initialized config
setup_logger()
logger = get_logger(__name__)

if __name__ == '__main__':
    logger.info("Starting up application...")
    logger.info(f"Configuration: PG_HOST={Config.config.pg_host}, PG_PORT={Config.config.pg_port}, PG_DATABASE={Config.config.pg_database}")

    Store.migrate_db(Config.config)

    logger.info(f"Starting Bottle server on {Config.config.port} port")
    run(host='0.0.0.0', port=Config.config.port)
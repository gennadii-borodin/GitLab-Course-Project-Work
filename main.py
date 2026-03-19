import os
import time
from psycopg2 import OperationalError
from data.config import Config


from bottle import Bottle, run
from datastore.store import Store
from utils.logger import setup_logger, get_logger
from api.db_plugin import DatabasePlugin
from api import login, things, user, static as static_routes, errors

# Initialize config FIRST before any other imports that might use logger
Config()



# Now setup logger with the initialized config
setup_logger()
logger = get_logger(__name__)


def wait_for_db(max_retries=30, delay=2):
    from datastore.connection import Connection
    for attempt in range(max_retries):
        try:
            with Connection(Config.config) as conn:
                conn.cursor().execute("SELECT 1")
            logger.info(f"Успешное подключение к БД на попытке {attempt + 1}")
            return
        except OperationalError, AttributeError:
            if attempt == max_retries - 1:
                raise
            logger.info(f"Попытка {attempt + 1} не удалась, повтор через {delay} секунд...")
            time.sleep(delay)

if __name__ == '__main__':
    logger.info("Starting up application...")
    logger.info(f"Configuration: PG_HOST={Config.config.pg_host}, PG_PORT={Config.config.pg_port}, PG_DATABASE={Config.config.pg_database}")
    logger.info(f"Configuration: PG_HOST={Config.config.port}, PG_PORT={Config.config},")
# Wait for database to be ready before migrations
    wait_for_db()
    logger.info("Database is ready, starting migrations...")
    Store.migrate_db(Config.config)
    # Create Bottle app and install database plugin
    app = Bottle()
    app.install(DatabasePlugin(Config.config))
    
    # Manually register all routes on this app
    # Auth routes
    app.post('/login', callback=login.do_login)
    app.post('/register', callback=login.register)
    
    # Things routes
    app.get('/things', callback=things.get_things)
    
    # User routes
    app.get('/user/current', callback=user.current_user)
    app.get('/user/<username>', callback=user.user_by_username)
    
    # Static routes
    app.get('/static/<filename>', callback=static_routes.server_static)
    app.get('/scripts/components/<filename>', callback=static_routes.server_script_component)
    app.get('/scripts/<filename>', callback=static_routes.server_script)
    app.get('/', callback=static_routes.index)
    app.get('/login', callback=static_routes.login)
    app.get('/restricted', callback=static_routes.restricted_area)
    app.get('/admin', callback=static_routes.admin_area)
    
    # Error handlers
    app.error(404, callback=errors.error404)
    app.error(500, callback=errors.error500)

    logger.info(f"Starting Bottle server on {Config.config.port} port")
    run(app=app, host='0.0.0.0', port=Config.config.port)

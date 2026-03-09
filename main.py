import os
from data.config import Config

# Initialize config FIRST before any other imports that might use logger
Config()

from bottle import Bottle, run
from datastore.store import Store
from utils.logger import setup_logger, get_logger
from api.db_plugin import DatabasePlugin
from api import login, things, user, static as static_routes, errors

# Now setup logger with the initialized config
setup_logger()
logger = get_logger(__name__)

if __name__ == '__main__':
    logger.info("Starting up application...")
    logger.info(f"Configuration: PG_HOST={Config.config.pg_host}, PG_PORT={Config.config.pg_port}, PG_DATABASE={Config.config.pg_database}")

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

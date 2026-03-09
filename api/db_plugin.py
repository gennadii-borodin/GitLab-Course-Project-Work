import inspect
from datastore.connection import Connection
from data.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


class DatabasePlugin:
    """Bottle plugin that provides a database connection to route handlers."""
    
    name = 'database'
    api = 2
    
    def __init__(self, config):
        self.config = config
        
    def setup(self, app):
        logger.info("Database plugin installed")
        
    def apply(self, callback, route):
        # Check if callback expects 'db' parameter
        sig = inspect.signature(callback)
        accepts_db = 'db' in sig.parameters
        
        if accepts_db:
            def wrapper(*args, **kwargs):
                with Connection(self.config) as db:
                    kwargs['db'] = db
                    return callback(*args, **kwargs)
            return wrapper
        else:
            return callback

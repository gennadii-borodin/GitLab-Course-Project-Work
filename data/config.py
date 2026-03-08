import os


class Config:

    config = None

    ENV_PG_HOST = 'SPW_PG_HOST'
    ENV_PG_PORT = 'SPW_PG_PORT'
    ENV_PG_USER = 'SPW_PG_USER'
    ENV_PG_PASSWORD = 'SPW_PG_PASSWORD'
    ENV_PG_DATABASE = 'SPW_PG_DATABASE'
    ENV_MIGRATIONS_FILENAME = 'SPW_MIGRATIONS_FILENAME'
    ENV_DATA_DIRECTORY = 'SPW_DATA_DIRECTORY'
    ENV_STATIC_FILES_DIRECTORY = 'SPW_STATIC_FILES_DIRECTORY'
    ENV_COOKIE_SECRET = 'SPW_COOKIE_SECRET'
    ENV_PASSWORD_SECRET = 'SPW_PASSWORD_SECRET'
    ENV_LOG_LEVEL = 'SPW_LOG_LEVEL'
    ENV_LOG_FILE = 'SPW_LOG_FILE'
    ENV_PORT = 'SPW_PORT'
    ENV_SESSION_TTL = 'SPW_SESSION_TTL'

    defaults = dict(
        SPW_PG_HOST='localhost',
        SPW_PG_PORT=5432,
        SPW_PG_USER='postgres',
        SPW_PG_PASSWORD='password',
        SPW_PG_DATABASE='simple_website',
        SPW_MIGRATIONS_FILENAME='migrations.json',
        SPW_DATA_DIRECTORY='data',                  # should be an absolute path
        SPW_STATIC_FILES_DIRECTORY='static',        # should be an absolute path
        SPW_COOKIE_SECRET='some-secret-value',
        SPW_PASSWORD_SECRET='some-other-secret-value',
        SPW_LOG_LEVEL='DEBUG',
        SPW_LOG_FILE='/app/logs/app.log',
        SPW_PORT=9999,
        SPW_SESSION_TTL=10
    )

    def __init__(self,
                 pg_host=None,
                 pg_port=None,
                 pg_user=None,
                 pg_password=None,
                 pg_database=None,
                 migrations_filename=None,
                 data_directory=None,
                 static_files_directory=None,
                 cookie_secret=None,
                 password_secret=None,
                 log_level=None,
                 log_file=None,
                 port=None,
                 session_ttl=None):
        self.pg_host = pg_host or os.getenv(Config.ENV_PG_HOST) or Config.defaults[Config.ENV_PG_HOST]
        self.pg_port = pg_port or os.getenv(Config.ENV_PG_PORT) or Config.defaults[Config.ENV_PG_PORT]
        self.pg_user = pg_user or os.getenv(Config.ENV_PG_USER) or Config.defaults[Config.ENV_PG_USER]
        self.pg_password = pg_password or os.getenv(Config.ENV_PG_PASSWORD) or Config.defaults[Config.ENV_PG_PASSWORD]
        self.pg_database = pg_database or os.getenv(Config.ENV_PG_DATABASE) or Config.defaults[Config.ENV_PG_DATABASE]
        self.migrations_filename = migrations_filename or os.getenv(Config.ENV_MIGRATIONS_FILENAME) or Config.defaults[Config.ENV_MIGRATIONS_FILENAME]
        self.data_directory = data_directory or os.getenv(Config.ENV_DATA_DIRECTORY) or Config.defaults[Config.ENV_DATA_DIRECTORY]
        self.static_files_directory = static_files_directory or os.getenv(Config.ENV_STATIC_FILES_DIRECTORY) or Config.defaults[Config.ENV_STATIC_FILES_DIRECTORY]
        self.cookie_secret = cookie_secret or os.getenv(Config.ENV_COOKIE_SECRET) or Config.defaults[Config.ENV_COOKIE_SECRET]
        self.password_secret = password_secret or os.getenv(Config.ENV_PASSWORD_SECRET) or Config.defaults[Config.ENV_PASSWORD_SECRET]
        self.log_level = log_level or os.getenv(Config.ENV_LOG_LEVEL) or Config.defaults[Config.ENV_LOG_LEVEL]
        self.log_file = log_file or os.getenv(Config.ENV_LOG_FILE) or Config.defaults[Config.ENV_LOG_FILE]
        self.port = port or os.getenv(Config.ENV_PORT) or Config.defaults[Config.ENV_PORT]
        self.session_ttl = session_ttl or os.getenv(Config.ENV_SESSION_TTL) or Config.defaults[Config.ENV_SESSION_TTL]
        Config.config = self

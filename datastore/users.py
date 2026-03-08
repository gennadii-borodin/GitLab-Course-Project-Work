import hashlib
from utils.logger import get_logger

logger = get_logger(__name__)


def calculate_password_hash(config, password):
    logger.debug("Calculating password hash")
    secret = config.password_secret
    module = hashlib.md5()
    string = f'{password}+{secret}'
    module.update(bytes(string, encoding='utf-8'))
    password_hash = module.hexdigest()
    return password_hash


def create_user(db, config, firstname, lastname, username, password):
    logger.debug(f"Creating user: username='{username}', firstname='{firstname}', lastname='{lastname}'")
    password_hash = calculate_password_hash(config, password)
    cursor = db.execute(
        'INSERT INTO users(firstname, lastname, created_at, is_admin) values(%s, %s, CURRENT_TIMESTAMP, 0) RETURNING id;',
        (firstname, lastname))
    row_count1 = cursor.rowcount
    user_id = cursor.fetchone()[0]

    if row_count1 > 0:
        logger.debug(f"User record created with id={user_id}")
        row_count2 = db.execute(
            "INSERT INTO auth_methods(user_id, username, password, type) values(%s, %s, %s, 'USERNAME_AND_PASSWORD');",
            (user_id, username, password_hash)).rowcount

        if row_count2 > 0:
            logger.info(f"User '{username}' created successfully with id={user_id}")
            return True
        else:
            logger.error(f"Failed to create auth_methods for user '{username}'")
    else:
        logger.error(f"Failed to create user record for '{username}'")

    return False


def check_login(db, config, username, password):
    logger.debug(f"Checking login for username='{username}'")
    password_hash = calculate_password_hash(config, password)
    cursor = db.execute(
        'SELECT user_id from auth_methods where username=%s and password=%s and type=\'USERNAME_AND_PASSWORD\'',
        (username, password_hash))
    row = cursor.fetchone()
    if row:
        user_id = int(row['user_id'])
        logger.debug(f"Login successful for username='{username}', user_id={user_id}")
        return user_id
    logger.warning(f"Login failed for username='{username}': invalid credentials")
    return -1


def check_admin(db, username):
    logger.debug(f"Checking admin status for username='{username}'")
    user = user_by_username(db, username)
    if user:
        is_admin = bool(user["is_admin"])
        logger.debug(f"User '{username}' admin status: {is_admin}")
        return is_admin
    else:
        logger.warning(f"User '{username}' not found when checking admin status")
        return False


def get_user_by_id(db, user_id):
    logger.debug(f"Fetching user by id={user_id}")
    cursor = db.execute('SELECT * from users where id=%s', (user_id,))
    row = cursor.fetchone()
    if row:
        user = dict(row)
        logger.debug(f"Found user id={user_id}, username={user.get('username', 'N/A')}")
        return user
    logger.warning(f"User with id={user_id} not found")
    return None


def user_by_username(db, username):
    logger.debug(f"Fetching user by username='{username}'")
    user_id = user_id_by_username(db, username)
    return get_user_by_id(db, user_id)


def user_id_by_username(db, username):
    logger.debug(f"Looking up user_id for username='{username}'")
    cursor = db.execute("SELECT user_id from auth_methods where username=%s and type='USERNAME_AND_PASSWORD'", (username,))
    row = cursor.fetchone()
    if row:
        user_id = int(row["user_id"])
        logger.debug(f"Found user_id={user_id} for username='{username}'")
        return user_id
    logger.warning(f"username='{username}' not found in auth_methods")
    return None
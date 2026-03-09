from bottle import request, response
from datastore import users
from data.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


def do_login(db):
    logger.debug(f"Login attempt from IP: {request.remote_addr}")
    username = request.json.get('username')
    password = request.json.get('password')
    user_id = users.check_login(db, Config.config, username, password)
    user = None
    if user_id > 0:
        user = users.get_user_by_id(db, user_id)
        name = f"{user['firstname']} {user['lastname']}"
        cookie_content = {
            'username': username,
            'client-ip': request.remote_addr,
            'real-name': name
        }
        response.set_cookie("account", cookie_content, secret=Config.config.cookie_secret, max_age=Config.config.session_ttl)
        logger.info(f"User '{username}' logged in successfully from IP: {request.remote_addr}")
    else:
        logger.warning(f"Failed login attempt for username '{username}' from IP: {request.remote_addr}")

    response.headers['Content-type'] = 'application/json'
    return dict(login_success=user is not None)


def register(db):
    logger.debug(f"Registration attempt from IP: {request.remote_addr}")
    firstname = request.json.get('firstname')
    lastname = request.json.get('lastname')
    username = request.json.get('username')
    password = request.json.get('password')
    error_msg = None
    if firstname is not None and lastname is not None and username is not None and password is not None:
        if users.user_by_username(db, username) is not None:
            registration_success = False
            error_msg = 'Username is already in use'
            logger.warning(f"Registration failed: username '{username}' already exists")
        else:
            registration_success = users.create_user(db, Config.config, firstname, lastname, username, password)
            if registration_success:
                logger.info(f"User '{username}' registered successfully")
            else:
                error_msg = 'Some random error occurred'
                logger.error(f"Registration failed for username '{username}': {error_msg}")
    else:
        registration_success = False
        error_msg = 'Mandatory information missing'
        logger.warning(f"Registration failed: missing mandatory fields")

    response.headers['Content-type'] = 'application/json'
    return dict(registration_success=registration_success,
                error_msg=error_msg)

from bottle import get, request, response, HTTPError
from datastore import users
from data.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


@get('/user/current')
def current_user(db):
    logger.debug("Request to /user/current")
    cookie_content = request.get_cookie("account", secret=Config.config.cookie_secret)
    if cookie_content:
        current_username = cookie_content['username']
        user = users.user_by_username(db, current_username)
        if user:
            logger.info(f"User '{current_username}' accessed their profile")
        else:
            logger.warning(f"User '{current_username}' not found")
        return user
    logger.warning("Unauthorized access attempt to /user/current")
    return HTTPError(401, 'Access denied')


@get('/user/<username>')
def user_by_username(db, username):
    logger.debug(f"Request to /user/{username}")
    cookie_content = request.get_cookie("account", secret=Config.config.cookie_secret)
    if cookie_content:
        current_username = cookie_content['username']
        if users.check_admin(db, current_username):
            user = users.user_by_username(db, username)
            if user:
                logger.info(f"Admin '{current_username}' accessed user '{username}' profile")
                return user
            else:
                logger.warning(f"User '{username}' not found")
        else:
            logger.warning(f"Non-admin user '{current_username}' attempted to access user '{username}' profile")
    else:
        logger.warning("Unauthorized access attempt to /user/<username>")
    return HTTPError(401, 'Access denied')


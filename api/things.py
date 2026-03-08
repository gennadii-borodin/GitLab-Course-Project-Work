from bottle import get
from datastore import things
from utils.logger import get_logger

logger = get_logger(__name__)


@get('/things')
def get_things(db):
    logger.debug("Request to /things")
    all_things = things.get_all_things(db)
    logger.info(f"Returned {len(all_things)} things")
    return dict(things=all_things)

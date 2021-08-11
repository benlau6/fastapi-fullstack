import logging

from app.db.init_db import init_db
from app.api.deps import get_user_collection, get_db, get_settings


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    init_db(get_user_collection(get_db(get_settings())))


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
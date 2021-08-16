import logging

from app.db.mongo import client


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    try:
        dbs = client.list_database_names()
        logger.info(dbs)
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()

import logging
import asyncio

from app.db.init_db import init_db
from app.db.session import AsyncSessionLocal


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    db = AsyncSessionLocal()
    await init_db(db)


async def main() -> None:
    logger.info("Creating initial data")
    await init()
    logger.info("Initial data created")


if __name__ == "__main__":
    asyncio.run(main())
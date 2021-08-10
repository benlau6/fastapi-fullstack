
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


async_engine  = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, echo=True, future=True)
AsyncSessionLocal = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)


async def get_db():
    try:
        db = await AsyncSessionLocal()
        yield db
    finally:
        db.close()
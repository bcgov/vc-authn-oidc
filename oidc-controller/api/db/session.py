from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from api.core.config import settings

from sqlmodel.ext.asyncio.session import AsyncSession

async_engine = create_async_engine(
    settings.SQLALCHEMY_DATABASE_URI,
    echo=settings.DB_ECHO_LOG,
    echo_pool=settings.DB_ECHO_LOG,
    pool_size=20,
    poolclass=QueuePool,
)


async def get_async_session():
    async_session = sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

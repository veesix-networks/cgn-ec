from collections.abc import AsyncGenerator
from typing import Annotated

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker
from sqlalchemy.pool import NullPool, AsyncAdaptedQueuePool
from fastapi import Depends

from cgnec_api.config import settings


def get_db_credentials():
    return f"postgresql+psycopg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"


def get_engine(
    database_uri: str = get_db_credentials(),
    no_pool: bool = False,
    timeout: int = 15,
    **kwargs,
) -> AsyncEngine:
    """Creates an Async Engine instance to use async with SQLModel.

    Args:
        database_uri:       Database URI/DSN to connect to.
        no_pool:            Set to True if you are debugging and don't
            want to pool connections.
        timeout:            Timeout in seconds.
        kwargs:             Keyworded arguments passed into create_async_engine.
    """
    return create_async_engine(
        str(database_uri),
        future=True,
        poolclass=NullPool if no_pool else AsyncAdaptedQueuePool,
        pool_timeout=timeout,
        pool_recycle=3600 * 4,  # Recycle after 4 hours
        **kwargs,
    )


def get_session(engine: AsyncEngine = get_engine(), **kwargs) -> AsyncSession:
    """Creates a new session which manages persistent operations to ORM objects.

    Args:
        engine:     AsyncEngine object (typically get_engine() function).
        kwargs:             Keyworded arguments passed into async_sessionmaker.
    """
    session = async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
        **kwargs,
    )
    return session


Engine = get_engine()
SessionLocal = get_session(engine=Engine)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Returns an Async Session"""
    async with SessionLocal() as session:
        yield session


async def init_db() -> None:
    """Creates all database tables"""
    async with SessionLocal() as session:
        await session.run_sync(SQLModel.metadata.create_all)


DatabaseDep = Annotated[AsyncSession, Depends(get_db)]

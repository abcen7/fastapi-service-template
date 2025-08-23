from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from app import app
from app.core.config import settings
from app.core.database import Base
from app.core.database.engine import get_async_session


@pytest.fixture(scope="session")
async def setup_test_db():
    engine = create_async_engine(settings.db.asyncpg_url, isolation_level="AUTOCOMMIT")
    async with engine.begin() as conn:
        result = await conn.execute(
            text(
                f"SELECT 1 FROM pg_database WHERE datname = '{settings.db.TEST_DB_NAME}'"
            )
        )
        exists = result.scalar()
        if not exists:
            await conn.execute(text(f"CREATE DATABASE {settings.db.TEST_DB_NAME}"))
    await engine.dispose()

    test_engine = create_async_engine(settings.db.test_asyncpg_url)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Remove test db if needed
    # async with create_async_engine(MAIN_DB_URL, isolation_level="AUTOCOMMIT").begin() as conn:
    #     await conn.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}"))
    await test_engine.dispose()


@pytest.fixture(scope="session")
async def async_engine() -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(settings.db.test_asyncpg_url, echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


@pytest.fixture
async def async_session(setup_test_db):
    engine = create_async_engine(settings.db.test_asyncpg_url, echo=True)
    async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session
        await session.rollback()
    await engine.dispose()


@pytest.fixture
async def client(async_session):
    app.dependency_overrides[get_async_session] = lambda: async_session
    async with AsyncClient(app=app, base_url="http://test") as c:
        yield c

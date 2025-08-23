from collections.abc import Generator
from typing import AsyncGenerator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.main import app


@pytest.fixture(scope="session", autouse=True)
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async_engine = create_async_engine(
        settings.db.asyncpg_url,
        echo=settings.db.ECHO_DEBUG_MODE,
    )
    async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)
    async with async_session_maker() as session:
        yield session


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c

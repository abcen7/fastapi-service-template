from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

async_engine = create_async_engine(
    settings.db.asyncpg_url,
    echo=settings.db.ECHO_DEBUG_MODE,
)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Creates a new async session for the current context.

    Returns:
        sqlalchemy.ext.asyncio.session.AsyncSession: The newly created async session.
    """
    async with async_session_maker() as session:
        yield session


def load_models() -> None:
    from app.users import User

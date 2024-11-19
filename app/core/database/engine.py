from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from app.core.settings import settings


async_engine = create_async_engine(settings.db.build_postgres_url(), echo=settings.db.echo_debug_mode)
async_session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Creates a new async session for the current context.

    Returns:
        sqlalchemy.ext.asyncio.session.AsyncSession: The newly created async session.
    """
    async with async_session_maker() as session:
        yield session


def with_async_session(func):
    """
    Decorator for async session.

    Args:
        func (function): The function to decorate.

    Returns:
        function: The decorated function.
    """

    async def wrapper(*args, **kwargs):
        if "session" in kwargs and kwargs["session"] is not None:
            return await func(*args, **kwargs)
        async for session in get_async_session():
            return await func(*args, session=session, **kwargs)

    return wrapper
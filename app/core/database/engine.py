from typing import AsyncGenerator, Callable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.settings import settings

async_engine = create_async_engine(
    settings.db.asyncpg_url.unicode_string(), echo=settings.db.ECHO_DEBUG_MODE
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


def load_models():
    from app.users.models import User

from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import with_async_session

from .models import User


class UsersRepository:
    @with_async_session
    async def create(self, user: User, session: AsyncSession) -> None:
        session.add(user)
        await session.commit()

    @with_async_session
    async def get_all(self, session: AsyncSession) -> Sequence[User]:
        query = await session.execute(select(User))
        return query.scalars().all()

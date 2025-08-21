from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database.engine import get_async_session
from .models import User


class UsersRepository:
    def __init__(
        self,
        session: Annotated[AsyncSession, Depends(get_async_session)],
    ):
        self._session = session

    async def create(
        self,
        user: User,
    ) -> None:
        self._session.add(user)
        await self._session.commit()

    async def get_all(
        self,
    ) -> Sequence[User]:
        query = await self._session.execute(select(User))
        return query.scalars().all()

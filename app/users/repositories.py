from typing import Annotated, Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database.engine import get_async_session
from ..core.repositories import BaseRepository
from .models import User
from .schemas import UserCreate


class UsersRepository(BaseRepository[User, UserCreate]):
    _db_model = User

    # async def create(
    #     self,
    #     user: User,
    # ) -> None:
    #     self._session.add(user)
    #     await self._session.commit()
    #
    # async def get_all(
    #     self,
    # ) -> Sequence[User]:
    #     query = await self._session.execute(select(User))
    #     return query.scalars().all()

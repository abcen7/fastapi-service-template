from typing import Annotated, Sequence

from fastapi import Depends

from .models import User
from .repositories import UsersRepository
from .schemas import UserCreate


class UsersService:
    def __init__(self, repository: Annotated[UsersRepository, Depends()]):
        self._repository = repository

    async def create(self, user: UserCreate) -> None:
        return await self._repository.create(User(**user.model_dump()))

    async def get_all(self) -> Sequence[User]:
        return await self._repository.get_all()

from .models import User
from .repositories import UsersRepository
from .schemas import UserCreate


class UsersService:
    repository = UsersRepository()

    async def __call__(self, *args, **kwargs):
        print("UserService object was just created")

    async def create(self, user: UserCreate) -> None:
        return await self.repository.create(User(**user.model_dump()))

    async def get_all(self) -> list[User]:
        return await self.repository.get_all()

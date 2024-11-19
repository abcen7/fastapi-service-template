from .models import User
from .schemas import UserCreate
from .repositories import UsersRepository


class UsersService:
    repository = UsersRepository()

    async def __call__(self, *args, **kwargs):
        print("UserService object was just created")

    async def create(self, user: UserCreate) -> User:
        return await self.repository.create(User(**user.model_dump()))

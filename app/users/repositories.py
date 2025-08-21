from ..core.repositories import BaseRepository
from .models import User
from .schemas import UserCreate


class UsersRepository(BaseRepository[User, UserCreate]):
    _db_model = User

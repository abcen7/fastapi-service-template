from typing import Annotated

from fastapi import APIRouter, Depends

from app.users.models import User
from app.users.schemas import UserCreate, UserResponse
from app.users.services import UsersService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse], status_code=200)
async def get_all(users_service: Annotated[UsersService, Depends()]):
    return await users_service.get_all()


@router.post("/", status_code=201)
async def create(
    users_service: Annotated[UsersService, Depends()], user: UserCreate
) -> None:
    return await users_service.create(user)

from datetime import datetime

from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    bio: str | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    bio: str | None = None
    created_at: datetime
    updated_at: datetime

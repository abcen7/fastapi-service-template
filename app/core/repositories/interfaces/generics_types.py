from typing import TypeVar

from pydantic import BaseModel

from app.core.database.base import Base

BaseORMModel = TypeVar("BaseORMModel", bound=Base)
DTO = TypeVar("DTO", bound=BaseModel)

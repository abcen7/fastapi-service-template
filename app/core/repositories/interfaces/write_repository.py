from abc import ABC, abstractmethod
from typing import Any, Generic

from pydantic import BaseModel

from ...database import Base


class IWriteRepository[
    BaseORMModel: Base,
    DTO: BaseModel,
](ABC):
    """
    Write only interface for implementing writing operations in database
    For clients which doesn't need the readable operations could be extended by IWriteRepository
    """

    @abstractmethod
    async def create(
        self,
        dto: DTO,
    ) -> BaseORMModel: ...

    @abstractmethod
    async def update(
        self,
        id_: int,
        **values: Any,
    ) -> BaseORMModel: ...

    @abstractmethod
    async def delete(
        self,
        id_: int,
    ) -> None: ...

    @abstractmethod
    async def create_many(
        self,
        dto_list: list[DTO],
    ) -> list[BaseORMModel]: ...

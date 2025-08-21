from abc import ABC, abstractmethod
from typing import Generic

from .generics_types import DTO, BaseORMModel


class IWriteRepository(
    ABC,
    Generic[BaseORMModel, DTO],
):
    """
    Write only interface for implementing writing operations in database
    For clients which doesn't need the readable operations could be extended by IWriteRepository
    """

    @abstractmethod
    async def create(
        self,
        dto: DTO,
    ) -> BaseORMModel:
        ...

    @abstractmethod
    async def update(
        self,
        id_: int,
        **values,
    ) -> BaseORMModel:
        ...

    @abstractmethod
    async def delete(
        self,
        id_: int,
    ) -> None:
        ...

    @abstractmethod
    async def create_many(
        self,
        dto_list: list[DTO],
    ) -> list[BaseORMModel]:
        ...

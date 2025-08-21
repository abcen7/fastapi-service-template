from abc import ABC, abstractmethod
from typing import Generic

from .generics_types import BaseORMModel


class IReadRepository(
    ABC,
    Generic[BaseORMModel],
):
    """
    Readonly interface for reading from database
    For clients which doesn't need the writeable operations could be extended by IReadRepository
    """

    @abstractmethod
    async def get_one(
        self,
        *where,
        **filter_by,
    ) -> BaseORMModel:
        ...

    @abstractmethod
    async def get_one_or_none(
        self,
        *where,
        **filter_by,
    ) -> BaseORMModel | None:
        ...

    @abstractmethod
    async def get_all(
        self,
        *where,
        **filter_by,
    ) -> list[BaseORMModel]:
        ...

    @abstractmethod
    async def count(
        self,
        *where,
        **filter_by,
    ) -> int:
        ...

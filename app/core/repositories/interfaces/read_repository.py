from abc import ABC, abstractmethod
from typing import Any

from sqlalchemy import ColumnExpressionArgument

from app.core.database import Base


class IReadRepository[BaseORMModel: Base](ABC):
    """
    Readonly interface for reading from database
    For clients which doesn't need the writeable operations could be extended by IReadRepository
    """

    @abstractmethod
    async def get_one(
        self,
        *where: ColumnExpressionArgument[bool],
        **filter_by: Any,
    ) -> BaseORMModel: ...

    @abstractmethod
    async def get_one_or_none(
        self,
        *where: ColumnExpressionArgument[bool],
        **filter_by: Any,
    ) -> BaseORMModel | None: ...

    @abstractmethod
    async def get_all(
        self,
        *where: ColumnExpressionArgument[bool],
        **filter_by: Any,
    ) -> list[BaseORMModel]: ...

    @abstractmethod
    async def count(
        self,
        *where: ColumnExpressionArgument[bool],
        **filter_by: Any,
    ) -> int: ...

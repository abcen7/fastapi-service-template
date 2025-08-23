from typing import Any

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy import ColumnExpressionArgument, delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import Base
from app.core.database.engine import get_async_session

from .interfaces import EntityNotFoundError, IRepository


class BaseRepository[BaseORMModel: Base, DTO: BaseModel](IRepository):
    """
    Base implementation of repository pattern with CRUD operations.
    Concrete repositories must set `_db_model`.
    """

    _db_model: type[BaseORMModel]

    def __init__(
        self,
        session: AsyncSession = Depends(get_async_session),
    ):
        self._session: AsyncSession = session

    def __init_subclass__(
        cls,
    ) -> None:
        """
        Ensure that the subclass has the `model` attribute defined.
        """
        if not hasattr(cls, "_db_model"):
            raise RuntimeError(f"{cls.__name__} is missing the `_db_model` attribute.")
        super().__init_subclass__()

    async def create(
        self,
        dto: DTO,
    ) -> BaseORMModel:
        """
        Creates a new record based on the DTO and returns the ORM instance.
        """
        instance = self._db_model(**dto.model_dump())
        self._session.add(instance)
        await self._session.commit()
        return instance

    async def create_many(
        self,
        dto_list: list[DTO],
    ) -> list[BaseORMModel]:
        """
        Performs bulk creation in a single transaction. Rolls back on error.
        """
        instances = [self._db_model(**dto.model_dump()) for dto in dto_list]
        self._session.add_all(instances)
        try:
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise
        return instances

    async def get_one(
        self,
        *where: ColumnExpressionArgument[bool],
        **filter_by: Any,
    ) -> BaseORMModel:
        """
        Returns a record by ID or raises EntityNotFoundError.
        """
        stmt = (
            select(self._db_model)
            .where(
                self._db_model.deleted_at.is_(None),
                *where,
            )
            .filter_by(**filter_by)
        )
        if (result := await self._session.scalar(stmt)) is None:
            raise EntityNotFoundError(self._db_model)
        return result

    async def get_one_or_none(
        self,
        *where: ColumnExpressionArgument[bool],
        **filter_by: Any,
    ) -> BaseORMModel | None:
        """
        Returns a record by ID or None if not found.
        """
        stmt = (
            select(self._db_model)
            .where(
                self._db_model.deleted_at.is_(None),
                *where,
            )
            .filter_by(**filter_by)
        )
        return await self._session.scalar(stmt)

    async def get_all(
        self,
        *where: ColumnExpressionArgument[bool],
        **filter_by: Any,
    ) -> list[BaseORMModel]:
        """
        Returns all records (excluding soft-deleted) that match additional conditions.
        """
        stmt = (
            select(self._db_model)
            .where(self._db_model.deleted_at.is_(None), *where)
            .filter_by(**filter_by)
        )
        result = await self._session.scalars(stmt)
        return list(result.unique().all())

    async def count(
        self,
        *where: ColumnExpressionArgument[bool],
        **filter_by: Any,
    ) -> int:
        """
        Counts records that match filters (excluding soft-deleted).
        """
        stmt = (
            select(func.count(self._db_model.id))
            .where(self._db_model.deleted_at.is_(None), *where)
            .filter_by(**filter_by)
        )
        result = await self._session.scalar(stmt)
        return result or 0

    async def update(
        self,
        id_: int,
        **values: Any,
    ) -> BaseORMModel:
        """
        Updates fields of the record by ID and returns the updated object.
        """
        if await self.get_one_or_none(self._db_model.id == id_) is None:
            raise EntityNotFoundError(self._db_model, id_)

        stmt = (
            update(self._db_model)
            .where(self._db_model.id == id_)
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        await self._session.execute(stmt)
        await self._session.commit()

        return await self.get_one(self._db_model.id == id_)

    async def delete(
        self,
        id_: int,
    ) -> None:
        """
        Soft-delete: sets deleted_at to current timestamp.
        """
        if await self.get_one_or_none(self._db_model.id == id_) is None:
            raise EntityNotFoundError(self._db_model, id_)

        stmt = (
            update(self._db_model)
            .where(self._db_model.id == id_)
            .values(deleted_at=func.now())
            .execution_options(synchronize_session="fetch")
        )
        await self._session.execute(stmt)
        await self._session.commit()

    async def hard_delete(
        self,
        id_: int,
    ) -> None:
        """
        Permanently deletes the record from the table (hard delete).
        """
        if await self.get_one_or_none(self._db_model.id == id_) is None:
            raise EntityNotFoundError(self._db_model, id_)

        stmt = delete(self._db_model).where(self._db_model.id == id_)
        await self._session.execute(stmt)
        await self._session.commit()

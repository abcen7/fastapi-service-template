from typing import Generic

from fastapi import Depends
from sqlalchemy import delete, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database.engine import get_async_session
from app.core.repositories.interfaces import (
    DTO,
    BaseORMModel,
    EntityNotFoundError,
    IRepository,
)


class BaseRepository(
    IRepository[BaseORMModel, DTO],
    Generic[BaseORMModel, DTO],
):
    """
    TODO: write the docs
    """

    model: type[BaseORMModel]

    def __init__(self, session: AsyncSession = Depends(get_async_session)):
        self._session: AsyncSession = session

    def __init_subclass__(cls) -> None:
        """
        Ensure that the subclass has the `model` attribute defined.
        """
        if not hasattr(cls, "model"):
            raise RuntimeError(f"{cls.__name__} is missing the `model` attribute.")
        super().__init_subclass__()

    async def create(self, dto: DTO) -> BaseORMModel:
        """
        Creates a new record based on the DTO and returns the ORM instance.
        """
        instance = self.model(**dto.model_dump())
        self._session.add(instance)
        await self._session.commit()
        return instance

    async def create_many(self, dto_list: list[DTO]) -> list[BaseORMModel]:
        """
        Performs bulk creation in a single transaction. Rolls back on error.
        """
        instances = [self.model(**dto.model_dump()) for dto in dto_list]
        self._session.add_all(instances)
        try:
            await self._session.commit()
        except Exception:
            await self._session.rollback()
            raise
        return instances

    async def get_one(self, *where, **filter_by) -> BaseORMModel:
        """
        Returns a record by ID or raises EntityNotFoundError.
        """
        stmt = (
            select(self.model)
            .where(
                self.model.deleted_at.is_(None),
                *where,
            )
            .filter_by(**filter_by)
        )
        if (result := await self._session.scalar(stmt)) is None:
            raise EntityNotFoundError(self.model)
        return result

    async def get_one_or_none(self, *where, **filter_by) -> BaseORMModel | None:
        """
        Returns a record by ID or None if not found.
        """
        stmt = (
            select(self.model)
            .where(
                self.model.deleted_at.is_(None),
                *where,
            )
            .filter_by(**filter_by)
        )
        return await self._session.scalar(stmt)

    async def get_all(
        self,
        *where: object,
        **filter_by: object,
    ) -> list[BaseORMModel]:
        """
        Returns all records (excluding soft-deleted) that match additional conditions.
        """
        stmt = (
            select(self.model)
            .where(self.model.deleted_at.is_(None), *where)
            .filter_by(**filter_by)
        )
        result = await self._session.scalars(stmt)
        return list(result.unique().all())

    async def count(
        self,
        *where,
        **filter_by,
    ) -> int:
        """
        Counts records that match filters (excluding soft-deleted).
        """
        stmt = (
            select(func.count(self.model.id))
            .where(self.model.deleted_at.is_(None), *where)
            .filter_by(**filter_by)
        )
        result = await self._session.scalar(stmt)
        return result or 0

    async def update(
        self,
        id_: int,
        **values,
    ) -> BaseORMModel:
        """
        Updates fields of the record by ID and returns the updated object.
        """
        if await self.get_one_or_none(self.model.id == id_) is None:
            raise EntityNotFoundError(self.model, id_)

        stmt = (
            update(self.model)
            .where(self.model.id == id_)
            .values(**values)
            .execution_options(synchronize_session="fetch")
        )
        await self._session.execute(stmt)
        await self._session.commit()

        return await self.get_one(id_)

    async def delete(
        self,
        id_: int,
    ) -> None:
        """
        Soft-delete: sets deleted_at to current timestamp.
        """
        if await self.get_one_or_none(self.model.id == id_) is None:
            raise EntityNotFoundError(self.model, id_)

        stmt = (
            update(self.model)
            .where(self.model.id == id_)
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
        if await self.get_one_or_none(self.model.id == id_) is None:
            raise EntityNotFoundError(self.model, id_)

        stmt = delete(self.model).where(self.model.id == id_)
        await self._session.execute(stmt)
        await self._session.commit()

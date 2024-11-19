from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        # TODO: change it to https://github.com/Netflix/dispatch/blob/master/src/dispatch/database/core.py#L51
        return f"{cls.__name__.lower()}"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(), default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(), default=func.now(), onupdate=func.now()
    )

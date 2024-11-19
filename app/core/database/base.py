from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import DateTime, func, Integer
from typing import Optional
from datetime import datetime


class Base(DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"

    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(), default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(), default=func.now(), onupdate=func.now()
    )

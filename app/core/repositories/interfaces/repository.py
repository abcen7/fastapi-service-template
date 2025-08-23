from abc import ABC

from pydantic import BaseModel

from app.core.database import Base

from .read_repository import IReadRepository
from .write_repository import IWriteRepository


class IRepository[
    BaseORMModel: Base,
    DTO: BaseModel,
](
    IReadRepository[BaseORMModel],
    IWriteRepository[BaseORMModel, DTO],
    ABC,
):
    """
    Full interface of repository for read/write operations
    """

    pass

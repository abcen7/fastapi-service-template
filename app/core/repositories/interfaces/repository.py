from abc import ABC

from .generics_types import DTO, BaseORMModel
from .read_repository import IReadRepository
from .write_repository import IWriteRepository


class IRepository(
    IReadRepository[BaseORMModel],
    IWriteRepository[BaseORMModel, DTO],
    ABC,
):
    """
    Full interface of repository for read/write operations
    """

    pass

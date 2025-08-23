from fastapi import HTTPException
from starlette import status

from app.core.database import Base


class EntityNotFoundError[BaseORMModel: Base](HTTPException):
    """If entity with specific id wasn't found"""

    def __init__(
        self,
        model_cls: type[BaseORMModel],
        id_: int | None = None,
    ):
        if id_ is not None:
            detail = f"The entity {model_cls.__name__} with id={id_} wasn't found."
        else:
            detail = f"The entity {model_cls.__name__} was not found."
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
        self.model_cls = model_cls
        self.id_ = id_

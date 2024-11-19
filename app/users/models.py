from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class User(Base):
    """
    Represents a user.

    Attributes:
        username (str): The user username.
        first_name (str): The user first name.
        last_name (str): The user last name.
    """

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(32))
    first_name: Mapped[str] = mapped_column(String(32))
    last_name: Mapped[str] = mapped_column(String(32))
    bio: Mapped[Optional[str]] = mapped_column(
        String(255), default=None, server_default=None
    )

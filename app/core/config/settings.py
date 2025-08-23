from typing import Annotated

from pydantic import UrlConstraints, computed_field
from pydantic_core import MultiHostUrl, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.lib import main_logger
from app.core.lib.databases import Databases, PostgreSQLDrivers

"""
TODO: Please, add the settings of all services right here.
"""

PostgresDsn = Annotated[
    MultiHostUrl,
    UrlConstraints(
        host_required=True,
        allowed_schemes=[
            "postgres",
            "postgresql",
            "postgresql+asyncpg",
            "postgresql+pg8000",
            "postgresql+psycopg",
            "postgresql+psycopg2",
            "postgresql+psycopg2cffi",
            "postgresql+py-postgresql",
            "postgresql+pygresql",
        ],
    ),
]


class DatabaseSettings(BaseSettings):
    """
    For default uses the Postgres
    """

    ECHO_DEBUG_MODE: bool = False
    USED: Databases = Databases.PostgreSQL
    HOST: str = "localhost"
    PORT: int = 5432
    USER: str = "postgres"
    PASSWORD: str = "postgres"
    NAME: str = "fst_db"

    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env")

    @computed_field
    def postgres_url(self) -> PostgresDsn:
        """
        This is a computed field that generates a PostgresDsn URL

        Returns:
            PostgresDsn: The constructed PostgresDsn URL.
        """
        return MultiHostUrl.build(
            scheme=PostgreSQLDrivers.DEFAULT_DIALECT,
            username=self.USER,
            password=self.PASSWORD,
            host=self.HOST,
            path=self.NAME,
        )

    @computed_field
    def asyncpg_url(self) -> PostgresDsn:
        """
        This is a computed field that generates a PostgresDsn URL for asyncpg.

        Returns:
            PostgresDsn: The constructed PostgresDsn URL for asyncpg.
        """
        return MultiHostUrl.build(
            scheme=f"{PostgreSQLDrivers.DEFAULT_DIALECT}+{PostgreSQLDrivers.DEFAULT_ASYNC_DRIVER}",
            username=self.USER,
            password=self.PASSWORD,
            host=self.HOST,
            path=self.NAME,
        )


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()


try:
    settings = Settings()
    main_logger.info(settings.db.asyncpg_url)
except ValidationError as e:
    main_logger.critical("Some environment variables are incorrect.")
    main_logger.critical("Error in .env, validate the app/core/config/settings.py")
    for error in e.errors():
        main_logger.critical(
            f"{error.get('type')} {error.get('loc')} {error.get('msg')}"
        )
    exit(1)

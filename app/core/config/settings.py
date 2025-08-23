from typing import ClassVar, Final

from pydantic_core import MultiHostUrl, ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.lib import main_logger
from app.core.lib.databases import Databases, PostgreSQLDrivers

"""
    This file represents the main config of all entire service
    Adjust the settings of internal\external params right here.
"""


class ApplicationSettings(BaseSettings):
    """
    Represents the application settings
    """

    API_V1_STR: Final[str] = "/api/v1"


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
    TEST_DB_NAME: Final[str] = "test_db"

    model_config = SettingsConfigDict(
        env_prefix="DB_",
        env_file=".env",
    )

    @property
    def postgres_url(self) -> str:
        return str(
            MultiHostUrl.build(
                scheme=PostgreSQLDrivers.DEFAULT_DIALECT,
                username=self.USER,
                password=self.PASSWORD,
                host=self.HOST,
                port=self.PORT,
                path=self.NAME,
            )
        )

    @property
    def asyncpg_url(self) -> str:
        return str(
            MultiHostUrl.build(
                scheme=f"{PostgreSQLDrivers.DEFAULT_DIALECT}+{PostgreSQLDrivers.DEFAULT_ASYNC_DRIVER}",
                username=self.USER,
                password=self.PASSWORD,
                host=self.HOST,
                port=self.PORT,
                path=self.NAME,
            )
        )

    @property
    def test_asyncpg_url(self) -> str:
        return str(
            MultiHostUrl.build(
                scheme=f"{PostgreSQLDrivers.DEFAULT_DIALECT}+{PostgreSQLDrivers.DEFAULT_ASYNC_DRIVER}",
                username=self.USER,
                password=self.PASSWORD,
                host=self.HOST,
                port=self.PORT,
                path=self.TEST_DB_NAME,
            )
        )


class Settings(BaseSettings):
    db: ClassVar[DatabaseSettings] = DatabaseSettings()
    app: ClassVar[ApplicationSettings] = ApplicationSettings()


try:
    settings = Settings()
except ValidationError as e:
    main_logger.critical("Some environment variables are incorrect.")
    main_logger.critical("Error in .env, validate the app/core/config/settings.py")
    for error in e.errors():
        main_logger.critical(
            f"{error.get('type')} {error.get('loc')} {error.get('msg')}"
        )
    exit(1)

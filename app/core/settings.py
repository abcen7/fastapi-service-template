from pydantic import PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.lib import main_logger
from app.core.lib.databases import Databases, PostgreSQLDrivers

"""
TODO: Please, add the settings of all services right here.
"""


class DatabaseSettings(BaseSettings):
    """
    For default uses the Postgres
    """

    ECHO_DEBUG_MODE: bool = False
    USED: Databases = Databases.PostgreSQL
    HOST: str
    PORT: int
    USER: str
    PASSWORD: str
    NAME: str

    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env")

    @computed_field
    @property
    def postgres_url(self) -> PostgresDsn:
        """
        This is a computed field that generates a PostgresDsn URL

        The URL is built using the MultiHostUrl.build method, which takes the following parameters:
        - scheme: The scheme of the URL. In this case, it is "postgres".
        - username: The username for the Postgres database, retrieved from the POSTGRES_USER environment variable.
        - password: The password for the Postgres database, retrieved from the POSTGRES_PASSWORD environment variable.
        - host: The host of the Postgres database, retrieved from the POSTGRES_HOST environment variable.
        - path: The path of the Postgres database, retrieved from the POSTGRES_DB environment variable.

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
    @property
    def asyncpg_url(self) -> PostgresDsn:
        """
        This is a computed field that generates a PostgresDsn URL for asyncpg.

        The URL is built using the MultiHostUrl.build method, which takes the following parameters:
        - scheme: The scheme of the URL. In this case, it is "postgresql+asyncpg".
        - username: The username for the Postgres database, retrieved from the POSTGRES_USER environment variable.
        - password: The password for the Postgres database, retrieved from the POSTGRES_PASSWORD environment variable.
        - host: The host of the Postgres database, retrieved from the POSTGRES_HOST environment variable.
        - path: The path of the Postgres database, retrieved from the POSTGRES_DB environment variable.

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


settings = Settings()

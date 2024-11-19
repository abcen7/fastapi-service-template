from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.lib import main_logger
from app.core.lib.databases import Databases, PostgreSQLDrivers

'''
TODO: Please, add the settings of all services right here.
'''


class DatabaseSettings(BaseSettings):
    """
    For default uses the Postgres
    """
    echo_debug_mode: bool = False
    used: Databases = Databases.PostgreSQL
    host: str
    user: str
    password: str
    name: str

    model_config = SettingsConfigDict(env_prefix="DB_", env_file="/.env")

    def build_postgres_url(self) -> str:
        return f"postgresql+{PostgreSQLDrivers.DEFAULT_ASYNC_DRIVER}://" f"{self.user}:{self.password}" f"@{self.ip}/{self.name}"


class Settings(BaseSettings):
    db: DatabaseSettings = DatabaseSettings()


settings = Settings()

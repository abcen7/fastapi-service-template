from enum import StrEnum


class Databases(StrEnum):
    PostgreSQL = "PostgreSQL"


class PostgreSQLDrivers(StrEnum):
    DEFAULT_DIALECT = "postgresql"
    DEFAULT_ASYNC_DRIVER = "asyncpg"

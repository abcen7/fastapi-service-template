from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Never, Optional

import asyncpg.exceptions
from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.cors import CORSMiddleware

from .exceptions import FailedConnectToDatabase
from .logger import main_logger
from .prometheus import setup_monitoring


def create_default_fastapi_app(
    title: str, prometheus_setup: Optional[bool] = False, **kwargs: Any
) -> FastAPI:
    """
    Create and configure a default FastAPI application with CORS middleware and optional Prometheus monitoring.

    This function sets up a FastAPI application with a custom lifespan, CORS middleware,
    and optionally adds Prometheus monitoring.

    Args:
        title (str): The title of the FastAPI application.
        prometheus_setup (bool, optional): Whether to set up Prometheus monitoring. Defaults to True.
        **kwargs: Additional keyword arguments to pass to the FastAPI constructor.

    Returns:
        FastAPI: A configured FastAPI application instance.

    """

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[Never]:
        from app.core.config import settings

        from ..database.engine import async_session_maker

        async with async_session_maker() as session:
            try:
                test_stmt = await session.execute(text("SELECT 1"))
                if test_stmt.scalar() != 1:
                    raise FailedConnectToDatabase from None
            except Exception as e:
                main_logger.fatal(f"Failed to connect to database: {e}")
                raise FailedConnectToDatabase from None

        main_logger.info(
            f"{title} fastapi app is successfully connected to database {settings.db.NAME}"
        )
        yield
        main_logger.info(f"Shutdown {title} fastapi app complete")

    app = FastAPI(
        title=title,
        lifespan=lifespan,
        **kwargs,
    )

    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if prometheus_setup:
        setup_monitoring(app)

    return app

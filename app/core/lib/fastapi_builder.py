from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Never, Optional

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

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

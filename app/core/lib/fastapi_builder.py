from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Callable, Never, Optional, TypeVar

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.lib import main_logger, setup_monitoring


def create_default_fastapi_app(
    title: str, prometheus_setup: Optional[bool] = False, **kwargs: FastAPI
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
        main_logger.info(f"{title} fastapi app is successfully connected to database")
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

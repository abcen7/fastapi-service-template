from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator


def setup_monitoring(app: FastAPI) -> None:
    Instrumentator().instrument(app).expose(app)

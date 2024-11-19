import uvicorn
from fastapi import FastAPI

from app.core import settings
from app.core.lib import create_default_fastapi_app

app: FastAPI = create_default_fastapi_app(title="FastAPI template service")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        port=8000,
        host="localhost",
    )

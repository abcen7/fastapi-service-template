import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI

from app.core import settings
from app.core.lib import create_default_fastapi_app
from app.core.router import api_router

load_dotenv()
app: FastAPI = create_default_fastapi_app(title="FastAPI template service")

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8000, host="localhost", reload=True)

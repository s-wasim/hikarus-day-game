from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import day as day_router
from app.api import health as health_router
from app.api.errors import register_handlers
from app.llm.client import OllamaClient
from app.logging_config import configure_logging
from app.middleware.request_id import RequestIDMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    configure_logging()
    app.state.ollama = OllamaClient()
    yield


app = FastAPI(title="Arcade AI Game API", version="0.1.0", lifespan=lifespan)

app.add_middleware(RequestIDMiddleware)
register_handlers(app)

app.include_router(health_router.router, prefix="/api/v1")
app.include_router(day_router.router, prefix="/api/v1")

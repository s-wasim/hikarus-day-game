from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from app.config import settings
from app.routers import commit, health, turn
from app.tree.loader import init_store

structlog.configure(
    processors=[
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer(),
    ],
    wrapper_class=structlog.make_filtering_bound_logger(
        getattr(__import__("logging"), settings.log_level, 20)
    ),
)

log = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_store(settings.turn_configs_dir)
    log.info("startup", turn_configs_dir=str(settings.turn_configs_dir))
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Hikaru's Day AI Engine", version="0.1.0", lifespan=lifespan)
    app.include_router(health.router)
    app.include_router(turn.router)
    app.include_router(commit.router)
    return app


app = create_app()

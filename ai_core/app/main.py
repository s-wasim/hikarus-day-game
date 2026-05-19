from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.config import settings
from app.prompt_engine.loader import init_loader
from app.routers import commit, health, turn

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
    init_loader(settings.prompts_dir)
    log.info("startup", prompts_dir=str(settings.prompts_dir), llm_provider=settings.llm_provider)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Hikaru's Day AI Engine", version="0.1.0", lifespan=lifespan)

    @app.exception_handler(FileNotFoundError)
    async def file_not_found_handler(request: Request, exc: FileNotFoundError) -> JSONResponse:
        return JSONResponse(status_code=500, content={"detail": str(exc)})

    app.include_router(health.router)
    app.include_router(turn.router)
    app.include_router(commit.router)

    return app


app = create_app()

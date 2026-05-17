from fastapi import APIRouter, Request
from pydantic import BaseModel

from app import __version__
from app.llm.client import OllamaClient

router = APIRouter()


class HealthResponse(BaseModel):
    status: str
    ollama_reachable: bool
    version: str


@router.get("/health", response_model=HealthResponse)
async def health(request: Request) -> HealthResponse:
    client: OllamaClient = request.app.state.ollama
    reachable = await client.health()
    return HealthResponse(status="ok", ollama_reachable=reachable, version=__version__)


@router.get("/version")
async def version() -> dict[str, str]:
    return {"version": __version__}

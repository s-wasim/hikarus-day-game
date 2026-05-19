from fastapi import APIRouter, Depends

from app.llm.provider import LLMProvider
from app.llm.registry import get_provider
from app.prompt_engine.builder import PromptBuilder
from app.prompt_engine.loader import get_loader
from app.schemas.conversation import TurnRequest, TurnResponse
from app.services.turn import run_turn

router = APIRouter(tags=["turn"])


def get_builder() -> PromptBuilder:
    return PromptBuilder(get_loader())


@router.post("/turn", response_model=TurnResponse)
async def turn(
    request: TurnRequest,
    provider: LLMProvider = Depends(get_provider),
    builder: PromptBuilder = Depends(get_builder),
) -> TurnResponse:
    return await run_turn(request, provider, builder)

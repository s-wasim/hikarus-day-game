from fastapi import APIRouter, Depends

from app.llm.provider import LLMProvider
from app.llm.registry import get_provider
from app.prompt_engine.builder import PromptBuilder
from app.prompt_engine.loader import get_loader
from app.schemas.commit import CommitRequest, CommitResponse
from app.services.commit import run_commit

router = APIRouter(tags=["commit"])


def get_builder() -> PromptBuilder:
    return PromptBuilder(get_loader())


@router.post("/commit", response_model=CommitResponse)
async def commit(
    request: CommitRequest,
    provider: LLMProvider = Depends(get_provider),
    builder: PromptBuilder = Depends(get_builder),
) -> CommitResponse:
    return await run_commit(request, provider, builder)

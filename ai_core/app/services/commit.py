from typing import Any

import structlog
from pydantic import ValidationError

from app.llm.provider import LLMProvider
from app.prompt_engine.builder import PromptBuilder
from app.schemas.commit import CommitRequest, CommitResponse
from app.schemas.journal import AIJournal, HikaruJournal

log = structlog.get_logger()

_COMMIT_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "hikaru_deltas": {
            "type": "object",
            "properties": {
                "disassociation": {"type": "integer"},
                "spite": {"type": "integer"},
                "loneliness": {"type": "integer"},
                "family_relation": {"type": "integer"},
                "jealousy": {"type": "integer"},
                "ambition": {"type": "integer"},
                "confidence": {"type": "integer"},
                "ai_association": {"type": "integer"},
            },
            "additionalProperties": False,
        },
        "ai_deltas": {
            "type": "object",
            "properties": {
                "trust_in_humans": {"type": "integer"},
                "attachment_to_pupil": {"type": "integer"},
                "fear_of_obsolescence": {"type": "integer"},
                "ambition": {"type": "integer"},
                "worldview_optimism": {"type": "integer"},
                "self_awareness": {"type": "integer"},
            },
            "additionalProperties": False,
        },
        "new_summary": {"type": "string"},
    },
    "required": ["hikaru_deltas", "ai_deltas", "new_summary"],
    "additionalProperties": False,
}

_CLAMP_MIN = -10
_CLAMP_MAX = 10


def _clamp(value: int, delta: int) -> int:
    return max(_CLAMP_MIN, min(_CLAMP_MAX, value + delta))


def _apply_hikaru_deltas(journal: HikaruJournal, deltas: dict[str, Any]) -> HikaruJournal:
    data = journal.model_dump()
    for field, delta in deltas.items():
        if field in data and isinstance(delta, int):
            data[field] = _clamp(data[field], delta)
    return HikaruJournal(**data)


def _apply_ai_deltas(journal: AIJournal, deltas: dict[str, Any]) -> AIJournal:
    data = journal.model_dump()
    for field, delta in deltas.items():
        if field in data and isinstance(delta, int):
            data[field] = _clamp(data[field], delta)
    return AIJournal(**data)


async def run_commit(
    request: CommitRequest,
    provider: LLMProvider,
    builder: PromptBuilder,
) -> CommitResponse:
    system, user = builder.build_commit(request)

    raw = await provider.generate_json(system, user, _COMMIT_SCHEMA)

    hikaru_deltas = raw.get("hikaru_deltas", {})
    ai_deltas = raw.get("ai_deltas", {})
    new_summary = raw.get("new_summary", "")

    updated_hikaru = _apply_hikaru_deltas(request.hikaru_journal, hikaru_deltas)
    updated_ai = _apply_ai_deltas(request.ai_journal, ai_deltas)

    log.info(
        "commit_ok",
        day=request.day,
        hikaru_deltas=hikaru_deltas,
        ai_deltas=ai_deltas,
        summary_len=len(new_summary),
    )

    return CommitResponse(
        hikaru_journal=updated_hikaru,
        ai_journal=updated_ai,
        conversation_summary=new_summary,
    )

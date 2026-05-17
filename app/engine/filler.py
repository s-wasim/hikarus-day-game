import json
import time

import structlog
from pydantic import BaseModel, Field, ValidationError

from app.engine.history import assemble_history
from app.llm.client import OllamaClient
from app.prompts.loader import get_base, get_filler, get_stage
from app.schemas.day import Branch, Chunks, DayRequest, DayResponse, JournalEntry, Turn, VALID_LEAF_IDS
from app.schemas.plan import DayPlan
from app.schemas.state import TraitDeltas

log = structlog.get_logger()

PATH_LITERAL_VALS = ("reset", "king", "bicycle", "body", "static")


# --- LLM-facing schemas (compact: 3 choice_themes instead of 39 leaf_themes) ---

class ChoiceThemes(BaseModel):
    a: str = Field(min_length=1)
    b: str = Field(min_length=1)
    c: str = Field(min_length=1)


class BranchLLM(BaseModel):
    incoming_theme: str | None = None
    ai_message: str = Field(min_length=1)
    chunks: Chunks
    # 3 entries instead of 39 — derived to full leaf_themes map by code
    choice_themes: ChoiceThemes


class TurnLLM(BaseModel):
    turn_index: int = Field(ge=0)
    branches: list[BranchLLM] = Field(min_length=1)


class DayResponseLLM(BaseModel):
    day: int = Field(ge=0)
    ai_stage: str
    themes: list[str] = Field(min_length=1)
    turns: list[TurnLLM] = Field(min_length=1)
    journal_entry: JournalEntry
    trait_deltas: TraitDeltas
    committed_path: str | None = None
    path_rationale: str | None = None


def _derive_leaf_themes(choice_themes: ChoiceThemes) -> dict[str, str]:
    """Expand 3-entry choice map to all 39 leaf IDs using the deepest slot's letter."""
    mapping = {"a": choice_themes.a, "b": choice_themes.b, "c": choice_themes.c}
    return {leaf_id: mapping[leaf_id[-1]] for leaf_id in VALID_LEAF_IDS}


def _convert(llm: DayResponseLLM) -> DayResponse:
    turns = [
        Turn(
            turn_index=t.turn_index,
            branches=[
                Branch(
                    incoming_theme=b.incoming_theme,
                    ai_message=b.ai_message,
                    chunks=b.chunks,
                    leaf_themes=_derive_leaf_themes(b.choice_themes),
                )
                for b in t.branches
            ],
        )
        for t in llm.turns
    ]
    return DayResponse(
        day=llm.day,
        ai_stage=llm.ai_stage,
        themes=llm.themes,
        turns=turns,
        journal_entry=llm.journal_entry,
        trait_deltas=llm.trait_deltas,
        committed_path=llm.committed_path,  # type: ignore[arg-type]
        path_rationale=llm.path_rationale,
    )


async def run_filler(
    client: OllamaClient,
    request: DayRequest,
    plan: DayPlan,
) -> DayResponse:
    history_text = assemble_history(request.history)
    stage_prompt = get_stage(request.day)
    system = "\n\n".join([get_base(), stage_prompt, get_filler()])

    plan_summary = (
        f"Day plan:\n"
        f"- turn_count: {plan.turn_count}\n"
        f"- themes: {plan.themes}\n"
        f"- beats:\n"
        + "\n".join(f"  Turn {i}: {beat}" for i, beat in enumerate(plan.beats))
    )

    user_msg = (
        f"Pupil name: {request.pupil_name}\n"
        f"Day: {request.day}\n"
        f"Trait state: {request.trait_state.model_dump()}\n"
        f"\n{history_text}\n\n{plan_summary}"
    )

    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user_msg},
    ]

    error_context: str | None = None
    for attempt in range(2):
        if error_context:
            messages.append(
                {
                    "role": "user",
                    "content": f"Your previous response was invalid: {error_context}. "
                    "Please output a fully valid DayResponse JSON.",
                }
            )

        t0 = time.monotonic()
        raw = await client.chat(
            messages,
            format=DayResponseLLM.model_json_schema(),
            temperature=0.8,
        )
        latency_ms = int((time.monotonic() - t0) * 1000)
        log.info(
            "filler_call",
            attempt=attempt,
            latency_ms=latency_ms,
            raw_len=len(raw),
        )

        try:
            llm_response = DayResponseLLM.model_validate_json(raw)
            return _convert(llm_response)
        except (ValidationError, json.JSONDecodeError) as exc:
            error_context = str(exc)[:500]
            log.warning("filler_validation_failed", attempt=attempt, error=error_context)

    raise ValueError(f"Filler failed after 2 attempts. Last error: {error_context}")

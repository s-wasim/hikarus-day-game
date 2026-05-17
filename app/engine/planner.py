import json
import time

import structlog
from pydantic import ValidationError

from app.engine.history import assemble_history
from app.llm.client import OllamaClient
from app.prompts.loader import get_base, get_planner, get_stage
from app.schemas.day import DayRequest
from app.schemas.plan import DayPlan

log = structlog.get_logger()

# Allowable turn count ranges by day stage
_TURN_RANGES: dict[int, tuple[int, int]] = {
    0: (2, 4),
    1: (2, 4),
    2: (3, 5),
    3: (3, 5),
    4: (4, 6),
    5: (4, 6),
    6: (5, 7),
    7: (5, 7),
    8: (5, 8),
    9: (5, 8),
}


def _turn_range(day: int) -> tuple[int, int]:
    return _TURN_RANGES.get(day, (2, 8))


async def run_planner(client: OllamaClient, request: DayRequest) -> DayPlan:
    history_text = assemble_history(request.history)
    lo, hi = _turn_range(request.day)

    stage_prompt = get_stage(request.day)
    system = "\n\n".join([get_base(), stage_prompt, get_planner()])
    system += f"\n\nIMPORTANT: turn_count MUST be between {lo} and {hi} inclusive."

    user_msg = (
        f"Pupil name: {request.pupil_name}\n"
        f"Day: {request.day}\n"
        f"Trait state: {request.trait_state.model_dump()}\n"
        f"\n{history_text}"
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
                    f"Please try again. turn_count must be {lo}-{hi}.",
                }
            )

        t0 = time.monotonic()
        raw = await client.chat(
            messages,
            format=DayPlan.model_json_schema(),
            temperature=0.3,
        )
        latency_ms = int((time.monotonic() - t0) * 1000)
        log.info("planner_call", attempt=attempt, latency_ms=latency_ms)

        try:
            plan = DayPlan.model_validate_json(raw)
            lo, hi = _turn_range(request.day)
            if not (lo <= plan.turn_count <= hi):
                error_context = (
                    f"turn_count={plan.turn_count} is out of range [{lo}, {hi}]"
                )
                continue
            return plan
        except (ValidationError, json.JSONDecodeError) as exc:
            error_context = str(exc)

    raise ValueError(f"Planner failed after 2 attempts: {error_context}")

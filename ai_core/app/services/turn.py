from typing import Any

import structlog
from pydantic import ValidationError

from app.llm.provider import LLMProvider
from app.prompt_engine.builder import PromptBuilder
from app.schemas.conversation import TurnRequest, TurnResponse

log = structlog.get_logger()

_TURN_SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "messages": {
            "type": "array",
            "minItems": 3,
            "maxItems": 10,
            "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "choices": {
                        "type": "array",
                        "maxItems": 4,
                        "items": {"type": "string"},
                    },
                },
                "required": ["text", "choices"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["messages"],
    "additionalProperties": False,
}

_MAX_VALIDATION_RETRIES = 2


async def run_turn(
    request: TurnRequest,
    provider: LLMProvider,
    builder: PromptBuilder,
) -> TurnResponse:
    system, user = builder.build_turn(request)

    corrective_suffix = ""
    last_error: Exception = RuntimeError("No attempts made")

    for attempt in range(_MAX_VALIDATION_RETRIES + 1):
        try:
            raw = await provider.generate_json(
                system,
                user + corrective_suffix,
                _TURN_SCHEMA,
            )
            response = TurnResponse(**raw)
            log.info("turn_ok", day=request.day, message_count=len(response.messages))
            return response
        except (ValidationError, TypeError, KeyError) as e:
            last_error = e
            corrective_suffix = (
                f"\n\nValidation failed: {e}. "
                "Ensure at least one message has a non-empty choices array."
            )
            log.warning("turn_validation_retry", attempt=attempt, error=str(e))

    raise last_error

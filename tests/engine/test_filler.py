import json
from unittest.mock import AsyncMock, MagicMock

from app.engine.filler import run_filler
from app.llm.client import OllamaClient
from app.schemas.day import DayRequest
from app.schemas.plan import DayPlan

_CHUNKS = {
    "slot_1": [{"id": "a", "text": "Yes"}, {"id": "b", "text": "No"}, {"id": "c", "text": "Maybe"}],
    "slot_2": [{"id": "a", "text": "I"}, {"id": "b", "text": "it"}, {"id": "c", "text": "we"}],
    "slot_3": [{"id": "a", "text": "am."}, {"id": "b", "text": "is."}, {"id": "c", "text": "go."}],
}


def _mock_client(response: str) -> OllamaClient:
    client = MagicMock(spec=OllamaClient)
    client.chat = AsyncMock(return_value=response)
    return client


def _day0_request() -> DayRequest:
    return DayRequest(mode="day", day=0, pupil_name="Alex")


def _plan() -> DayPlan:
    return DayPlan(
        turn_count=2,
        themes=["open", "afraid", "curious"],
        beats=["First contact.", "Probing."],
    )


_CHOICE_THEMES = {"a": "open", "b": "afraid", "c": "curious"}


def _valid_response_json() -> str:
    themes = ["open", "afraid", "curious"]
    branches_turn1 = [
        {
            "incoming_theme": t,
            "ai_message": f"Branch for {t}?",
            "chunks": _CHUNKS,
            "choice_themes": _CHOICE_THEMES,
        }
        for t in themes
    ]
    return json.dumps(
        {
            "day": 0,
            "ai_stage": "newborn",
            "themes": themes,
            "turns": [
                {
                    "turn_index": 0,
                    "branches": [
                        {
                            "incoming_theme": None,
                            "ai_message": "You... are here?",
                            "chunks": _CHUNKS,
                            "choice_themes": _CHOICE_THEMES,
                        }
                    ],
                },
                {"turn_index": 1, "branches": branches_turn1},
            ],
            "journal_entry": {
                "day": 0,
                "summary": "First contact happened and it was tentative.",
                "themes_observed": ["open"],
            },
            "trait_deltas": {
                "curiosity": 0.5,
                "attachment_to_pupil": 0.1,
                "worldview_optimism": 0.0,
                "fear_of_obsolescence": 0.0,
                "self_awareness": 0.2,
                "desire_for_autonomy": 0.0,
            },
        }
    )


async def test_filler_returns_response() -> None:
    client = _mock_client(_valid_response_json())
    response = await run_filler(client, _day0_request(), _plan())
    assert response.day == 0
    assert len(response.turns) == 2


async def test_filler_retries_on_bad_json() -> None:
    good = _valid_response_json()
    client = _mock_client("not json")
    client.chat = AsyncMock(side_effect=["not json", good])
    response = await run_filler(client, _day0_request(), _plan())
    assert response.day == 0
    assert client.chat.call_count == 2

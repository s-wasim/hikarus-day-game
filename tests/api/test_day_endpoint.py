from unittest.mock import AsyncMock, patch

from httpx import AsyncClient

from app.schemas.day import VALID_LEAF_IDS

_CHUNKS = {
    "slot_1": [{"id": "a", "text": "Yes"}, {"id": "b", "text": "No"}, {"id": "c", "text": "Maybe"}],
    "slot_2": [{"id": "a", "text": "I"}, {"id": "b", "text": "it"}, {"id": "c", "text": "we"}],
    "slot_3": [{"id": "a", "text": "am."}, {"id": "b", "text": "is."}, {"id": "c", "text": "go."}],
}

_ZERO_TRAITS = {
    "curiosity": 0,
    "attachment_to_pupil": 0,
    "worldview_optimism": 0,
    "fear_of_obsolescence": 0,
    "self_awareness": 0,
    "desire_for_autonomy": 0,
}


def _make_leaf_themes(themes: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for i, leaf_id in enumerate(sorted(VALID_LEAF_IDS)):
        result[leaf_id] = themes[i % len(themes)]
    return result


def _valid_day_response() -> dict:
    themes = ["open", "afraid", "curious"]
    leaf_themes = _make_leaf_themes(themes)
    branch = {
        "incoming_theme": None,
        "ai_message": "You... are here?",
        "chunks": _CHUNKS,
        "leaf_themes": leaf_themes,
    }
    return {
        "day": 0,
        "ai_stage": "newborn",
        "themes": themes,
        "turns": [{"turn_index": 0, "branches": [branch]}],
        "journal_entry": {"day": 0, "summary": "First contact.", "themes_observed": ["open"]},
        "trait_deltas": {**_ZERO_TRAITS, "curiosity": 0.5},
    }


def _day0_request_body() -> dict:
    return {
        "mode": "day",
        "day": 0,
        "pupil_name": "Alex",
        "trait_state": _ZERO_TRAITS,
        "history": {"journal_entries": [], "last_day_transcript": None},
    }


async def test_day_endpoint_returns_200(async_client: AsyncClient) -> None:
    from app.schemas.day import DayResponse
    from app.schemas.plan import DayPlan

    plan = DayPlan(turn_count=2, themes=["open", "afraid", "curious"], beats=["Beat 0", "Beat 1"])
    response = DayResponse.model_validate(_valid_day_response())

    with (
        patch("app.api.day.run_planner", new=AsyncMock(return_value=plan)),
        patch("app.api.day.run_filler", new=AsyncMock(return_value=response)),
    ):
        resp = await async_client.post("/api/v1/day", json=_day0_request_body())

    assert resp.status_code == 200
    data = resp.json()
    assert data["day"] == 0
    assert "themes" in data


async def test_day_endpoint_bad_request(async_client: AsyncClient) -> None:
    resp = await async_client.post("/api/v1/day", json={"mode": "bad"})
    assert resp.status_code == 422


async def test_day_endpoint_llm_down(async_client: AsyncClient) -> None:
    from app.llm.client import LLMUnavailableError

    with patch("app.api.day.run_planner", new=AsyncMock(side_effect=LLMUnavailableError("down"))):
        resp = await async_client.post("/api/v1/day", json=_day0_request_body())

    assert resp.status_code == 503
    assert resp.json()["error"] == "llm_unavailable"

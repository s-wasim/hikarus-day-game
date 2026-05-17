import json
from unittest.mock import AsyncMock, MagicMock

from app.engine.planner import _turn_range, run_planner
from app.llm.client import OllamaClient
from app.schemas.day import DayRequest


def _mock_client(response: str) -> OllamaClient:
    client = MagicMock(spec=OllamaClient)
    client.chat = AsyncMock(return_value=response)
    return client


def _day0_request() -> DayRequest:
    return DayRequest(mode="day", day=0, pupil_name="Alex")


def _valid_plan_json(turn_count: int = 3) -> str:
    return json.dumps({
        "turn_count": turn_count,
        "themes": ["open", "afraid", "curious"],
        "beats": [f"Beat {i}" for i in range(turn_count)],
    })


async def test_planner_returns_plan() -> None:
    client = _mock_client(_valid_plan_json(3))
    plan = await run_planner(client, _day0_request())
    assert plan.turn_count == 3
    assert len(plan.themes) == 3


def test_turn_range_day_0() -> None:
    lo, hi = _turn_range(0)
    assert lo == 2
    assert hi == 4


def test_turn_range_day_7() -> None:
    lo, hi = _turn_range(7)
    assert lo == 5
    assert hi == 7


async def test_planner_retries_on_invalid_json() -> None:
    good = _valid_plan_json(3)
    client = _mock_client("not json")
    client.chat = AsyncMock(side_effect=["not json", good])
    plan = await run_planner(client, _day0_request())
    assert plan.turn_count == 3
    assert client.chat.call_count == 2


async def test_planner_retries_on_out_of_range_turn_count() -> None:
    bad = _valid_plan_json(turn_count=8)  # Day 0 max is 4
    good = _valid_plan_json(turn_count=3)
    client = _mock_client(bad)
    client.chat = AsyncMock(side_effect=[bad, good])
    plan = await run_planner(client, _day0_request())
    assert plan.turn_count == 3

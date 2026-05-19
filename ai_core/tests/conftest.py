from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.llm.provider import LLMProvider
from app.llm.registry import get_provider
from app.prompt_engine.loader import init_loader
from app.routers.commit import get_builder as commit_get_builder
from app.routers.turn import get_builder as turn_get_builder

PROMPTS_DIR = Path(__file__).parent.parent / "prompts"

_STUB_TURN_RESPONSE: dict[str, Any] = {
    "messages": [
        {"text": "...", "choices": []},
        {"text": "What?", "choices": []},
        {"text": "You?", "choices": ["Hikaru.", "...", "Who are you?"]},
    ]
}

_STUB_COMMIT_RESPONSE: dict[str, Any] = {
    "hikaru_deltas": {"loneliness": -1, "ai_association": 1},
    "ai_deltas": {"attachment_to_pupil": 1},
    "new_summary": "Hikaru introduced himself to the AI on Day 0.",
}


class StubLLMProvider:
    def __init__(self, response: dict[str, Any]) -> None:
        self._response = response

    async def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: dict[str, Any],
        *,
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> dict[str, Any]:
        return self._response


@pytest.fixture()
def turn_stub_provider() -> StubLLMProvider:
    return StubLLMProvider(_STUB_TURN_RESPONSE)


@pytest.fixture()
def commit_stub_provider() -> StubLLMProvider:
    return StubLLMProvider(_STUB_COMMIT_RESPONSE)


@pytest.fixture(autouse=True)
def _init_loader() -> None:
    init_loader(PROMPTS_DIR)


@pytest.fixture()
def turn_client(turn_stub_provider: StubLLMProvider) -> TestClient:
    from app.main import app

    app.dependency_overrides[get_provider] = lambda: turn_stub_provider
    app.dependency_overrides[turn_get_builder] = lambda: _make_builder()
    client = TestClient(app, raise_server_exceptions=True)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def commit_client(commit_stub_provider: StubLLMProvider) -> TestClient:
    from app.main import app

    app.dependency_overrides[get_provider] = lambda: commit_stub_provider
    app.dependency_overrides[commit_get_builder] = lambda: _make_builder()
    client = TestClient(app, raise_server_exceptions=True)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def plain_client() -> TestClient:
    from app.main import app

    client = TestClient(app, raise_server_exceptions=True)
    return client


def _make_builder():
    from app.prompt_engine.builder import PromptBuilder
    from app.prompt_engine.loader import get_loader

    return PromptBuilder(get_loader())

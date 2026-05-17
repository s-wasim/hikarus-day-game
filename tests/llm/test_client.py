import pytest
from pytest_httpx import HTTPXMock

from app.llm.client import LLMUnavailableError, OllamaClient


@pytest.fixture
def client() -> OllamaClient:
    return OllamaClient(base_url="http://testollama", model="test-model")


async def test_health_true(httpx_mock: HTTPXMock, client: OllamaClient) -> None:
    httpx_mock.add_response(url="http://testollama/api/tags", status_code=200)
    assert await client.health() is True


async def test_health_false_on_error(client: OllamaClient) -> None:
    result = await client.health()
    assert result is False


async def test_chat_returns_content(httpx_mock: HTTPXMock, client: OllamaClient) -> None:
    httpx_mock.add_response(
        url="http://testollama/api/chat",
        json={"message": {"content": "hello there"}},
    )
    result = await client.chat([{"role": "user", "content": "say hello"}])
    assert result == "hello there"


async def test_chat_request_body(httpx_mock: HTTPXMock, client: OllamaClient) -> None:
    httpx_mock.add_response(
        url="http://testollama/api/chat",
        json={"message": {"content": "ok"}},
    )
    await client.chat([{"role": "user", "content": "hi"}], temperature=0.3)
    request = httpx_mock.get_requests()[0]
    import json

    body = json.loads(request.content)
    assert body["model"] == "test-model"
    assert body["stream"] is False
    assert body["options"]["temperature"] == 0.3


async def test_chat_raises_on_network_error(client: OllamaClient) -> None:
    with pytest.raises(LLMUnavailableError):
        await client.chat([{"role": "user", "content": "hi"}])


async def test_schema_constrained_call(httpx_mock: HTTPXMock, client: OllamaClient) -> None:
    httpx_mock.add_response(
        url="http://testollama/api/chat",
        json={"message": {"content": '{"foo": 1}'}},
    )
    result = await client.chat(
        [{"role": "user", "content": "hi"}],
        format={"type": "object", "properties": {"foo": {"type": "integer"}}},
    )
    assert '"foo"' in result

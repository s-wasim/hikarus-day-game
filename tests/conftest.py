import pytest
from httpx import ASGITransport, AsyncClient

from app.llm.client import OllamaClient
from app.logging_config import configure_logging
from app.main import app


@pytest.fixture
async def async_client() -> AsyncClient:
    configure_logging()
    app.state.ollama = OllamaClient()
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client  # type: ignore[misc]

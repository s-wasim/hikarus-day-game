from unittest.mock import AsyncMock

from httpx import AsyncClient


async def test_health_returns_200(async_client: AsyncClient) -> None:
    from app.main import app

    app.state.ollama.health = AsyncMock(return_value=True)  # type: ignore[method-assign]
    resp = await async_client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert "version" in data


async def test_health_ollama_down(async_client: AsyncClient) -> None:
    from app.main import app

    app.state.ollama.health = AsyncMock(return_value=False)  # type: ignore[method-assign]
    resp = await async_client.get("/api/v1/health")
    assert resp.status_code == 200
    assert resp.json()["ollama_reachable"] is False


async def test_version_endpoint(async_client: AsyncClient) -> None:
    resp = await async_client.get("/api/v1/version")
    assert resp.status_code == 200
    assert "version" in resp.json()

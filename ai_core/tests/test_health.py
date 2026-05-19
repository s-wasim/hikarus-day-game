from fastapi.testclient import TestClient


def test_health_returns_ok(plain_client: TestClient) -> None:
    response = plain_client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert "version" in body

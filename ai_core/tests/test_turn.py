from fastapi.testclient import TestClient

_BASE_HIKARU = {
    "disassociation": 0,
    "spite": 0,
    "loneliness": 0,
    "family_relation": 0,
    "jealousy": 0,
    "ambition": 0,
    "confidence": 0,
    "ai_association": 5,
}

_BASE_AI = {
    "trust_in_humans": 0,
    "attachment_to_pupil": 0,
    "fear_of_obsolescence": 0,
    "ambition": 0,
    "worldview_optimism": 0,
    "self_awareness": 0,
}

_VALID_TURN_REQUEST = {
    "day": 0,
    "hikaru_journal": _BASE_HIKARU,
    "ai_journal": _BASE_AI,
}


def test_turn_returns_file_key_and_tree(turn_client: TestClient) -> None:
    response = turn_client.post("/turn", json=_VALID_TURN_REQUEST)
    assert response.status_code == 200
    body = response.json()
    assert "file_key" in body
    assert "tree" in body


def test_turn_day0_selects_generic(turn_client: TestClient) -> None:
    response = turn_client.post("/turn", json=_VALID_TURN_REQUEST)
    assert response.json()["file_key"] == "generic"


def test_turn_day1_selects_by_journal(turn_client: TestClient) -> None:
    req = {
        **_VALID_TURN_REQUEST,
        "day": 1,
        "ai_journal": {**_BASE_AI, "attachment_to_pupil": 8},
    }
    response = turn_client.post("/turn", json=req)
    assert response.json()["file_key"] == "attachment_to_pupil"


def test_turn_invalid_day_returns_422(turn_client: TestClient) -> None:
    bad = {**_VALID_TURN_REQUEST, "day": 99}
    response = turn_client.post("/turn", json=bad)
    assert response.status_code == 422


def test_turn_missing_file_returns_404(turn_client: TestClient) -> None:
    req = {**_VALID_TURN_REQUEST, "day": 5}
    response = turn_client.post("/turn", json=req)
    assert response.status_code == 404

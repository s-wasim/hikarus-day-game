import pytest
from fastapi.testclient import TestClient


_VALID_TURN_REQUEST = {
    "day": 0,
    "hikaru_journal": {
        "disassociation": 1,
        "spite": 2,
        "loneliness": 3,
        "family_relation": -1,
        "jealousy": 1,
        "ambition": -2,
        "confidence": -1,
        "ai_association": 5,
    },
    "ai_journal": {
        "trust_in_humans": 0,
        "attachment_to_pupil": 0,
        "fear_of_obsolescence": 0,
        "ambition": 0,
        "worldview_optimism": 0,
        "self_awareness": 0,
    },
    "conversation_summary": "",
}


def test_turn_returns_messages_and_choices(turn_client: TestClient) -> None:
    response = turn_client.post("/turn", json=_VALID_TURN_REQUEST)
    assert response.status_code == 200
    body = response.json()
    assert "messages" in body
    assert len(body["messages"]) >= 3
    has_choices = any(len(m["choices"]) > 0 for m in body["messages"])
    assert has_choices


def test_turn_message_structure(turn_client: TestClient) -> None:
    response = turn_client.post("/turn", json=_VALID_TURN_REQUEST)
    assert response.status_code == 200
    for msg in response.json()["messages"]:
        assert "text" in msg
        assert "choices" in msg
        assert isinstance(msg["choices"], list)
        assert len(msg["choices"]) <= 4


def test_turn_invalid_day_returns_422(turn_client: TestClient) -> None:
    bad_request = {**_VALID_TURN_REQUEST, "day": 99}
    response = turn_client.post("/turn", json=bad_request)
    assert response.status_code == 422


def test_turn_invalid_journal_value_returns_422(turn_client: TestClient) -> None:
    bad_journal = {**_VALID_TURN_REQUEST}
    bad_journal["hikaru_journal"] = {**bad_journal["hikaru_journal"], "disassociation": 100}
    response = turn_client.post("/turn", json=bad_journal)
    assert response.status_code == 422

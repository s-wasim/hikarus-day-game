from fastapi.testclient import TestClient


_VALID_COMMIT_REQUEST = {
    "day": 0,
    "hikaru_journal": {
        "disassociation": 0,
        "spite": 0,
        "loneliness": 3,
        "family_relation": 0,
        "jealousy": 0,
        "ambition": 0,
        "confidence": 0,
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
    "prior_messages": [
        {"text": "...", "choices": []},
        {"text": "What?", "choices": []},
        {"text": "You?", "choices": ["Hikaru.", "...", "Who are you?"]},
    ],
    "picked_choices": [
        {"message_index": 2, "choice_index": 0, "choice_text": "Hikaru."}
    ],
}


def test_commit_returns_updated_journals(commit_client: TestClient) -> None:
    response = commit_client.post("/commit", json=_VALID_COMMIT_REQUEST)
    assert response.status_code == 200
    body = response.json()
    assert "hikaru_journal" in body
    assert "ai_journal" in body
    assert "conversation_summary" in body


def test_commit_applies_deltas(commit_client: TestClient) -> None:
    response = commit_client.post("/commit", json=_VALID_COMMIT_REQUEST)
    body = response.json()
    # stub returns loneliness: -1, ai_association: +1
    assert body["hikaru_journal"]["loneliness"] == 2   # was 3, delta -1
    assert body["hikaru_journal"]["ai_association"] == 6  # was 5, delta +1
    # stub returns attachment_to_pupil: +1
    assert body["ai_journal"]["attachment_to_pupil"] == 1


def test_commit_returns_summary(commit_client: TestClient) -> None:
    response = commit_client.post("/commit", json=_VALID_COMMIT_REQUEST)
    body = response.json()
    assert len(body["conversation_summary"]) > 0


def test_commit_delta_clamping(commit_client: TestClient) -> None:
    req = dict(_VALID_COMMIT_REQUEST)
    req["hikaru_journal"] = {**req["hikaru_journal"], "loneliness": 9}
    response = commit_client.post("/commit", json=req)
    body = response.json()
    # loneliness was 9, delta -1 from stub -> should be 8
    assert body["hikaru_journal"]["loneliness"] == 8


def test_commit_invalid_request_returns_422(commit_client: TestClient) -> None:
    bad = dict(_VALID_COMMIT_REQUEST)
    bad.pop("prior_messages")
    response = commit_client.post("/commit", json=bad)
    assert response.status_code == 422

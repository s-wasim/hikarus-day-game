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

_ONE_PICK = [
    {
        "node_id": "0_0",
        "choice_index": 0,
        "ai_delta_favored": "attachment_to_pupil",
        "hikaru_delta_favored": "loneliness",
    }
]

_VALID_COMMIT_REQUEST = {
    "day": 0,
    "hikaru_journal": _BASE_HIKARU,
    "ai_journal": _BASE_AI,
    "picked_choices": _ONE_PICK,
}


def test_commit_returns_updated_journals(commit_client: TestClient) -> None:
    response = commit_client.post("/commit", json=_VALID_COMMIT_REQUEST)
    assert response.status_code == 200
    body = response.json()
    assert "hikaru_journal" in body
    assert "ai_journal" in body


def test_commit_single_pick_increments_deltas(commit_client: TestClient) -> None:
    req = {**_VALID_COMMIT_REQUEST, "hikaru_journal": {**_BASE_HIKARU, "loneliness": 3}}
    response = commit_client.post("/commit", json=req)
    body = response.json()
    assert body["hikaru_journal"]["loneliness"] == 4
    assert body["ai_journal"]["attachment_to_pupil"] == 1


def test_commit_multiple_picks_accumulate(commit_client: TestClient) -> None:
    req = {
        **_VALID_COMMIT_REQUEST,
        "picked_choices": [
            {
                "node_id": "0_0",
                "choice_index": 0,
                "ai_delta_favored": "attachment_to_pupil",
                "hikaru_delta_favored": "loneliness",
            },
            {
                "node_id": "1_1",
                "choice_index": 0,
                "ai_delta_favored": "attachment_to_pupil",
                "hikaru_delta_favored": "loneliness",
            },
        ],
    }
    response = commit_client.post("/commit", json=req)
    body = response.json()
    assert body["ai_journal"]["attachment_to_pupil"] == 2
    assert body["hikaru_journal"]["loneliness"] == 2


def test_commit_clamping_at_max(commit_client: TestClient) -> None:
    req = {
        **_VALID_COMMIT_REQUEST,
        "hikaru_journal": {**_BASE_HIKARU, "loneliness": 10},
    }
    response = commit_client.post("/commit", json=req)
    body = response.json()
    assert body["hikaru_journal"]["loneliness"] == 10


def test_commit_invalid_delta_name_returns_422(commit_client: TestClient) -> None:
    req = {
        **_VALID_COMMIT_REQUEST,
        "picked_choices": [
            {
                "node_id": "0_0",
                "choice_index": 0,
                "ai_delta_favored": "not_a_real_delta",
                "hikaru_delta_favored": "loneliness",
            }
        ],
    }
    response = commit_client.post("/commit", json=req)
    assert response.status_code == 422

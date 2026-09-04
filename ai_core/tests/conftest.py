import json
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.tree.loader import TreeStore, get_store, init_store

_TURN_CONFIGS_DIR = Path(__file__).parent.parent / "turn_configs"

_TINY_TREE = {
    "0_0": {
        "ai": "You are here.",
        "user": [
            {
                "text": "Yes.",
                "ai_delta_favored": "attachment_to_pupil",
                "hikaru_delta_favored": "loneliness",
            },
            {
                "text": "No.",
                "ai_delta_favored": "trust_in_humans",
                "hikaru_delta_favored": "spite",
            },
        ],
    }
}


@pytest.fixture(autouse=True)
def _init_store() -> None:
    init_store(_TURN_CONFIGS_DIR)


@pytest.fixture()
def tree_store(tmp_path: Path) -> TreeStore:
    (tmp_path / "day0").mkdir()
    (tmp_path / "day0" / "generic.json").write_text(json.dumps(_TINY_TREE))
    (tmp_path / "day1").mkdir()
    for key in [
        "trust_in_humans",
        "attachment_to_pupil",
        "fear_of_obsolescence",
        "ambition",
        "worldview_optimism",
        "self_awareness",
    ]:
        (tmp_path / "day1" / f"{key}.json").write_text(json.dumps(_TINY_TREE))
    store = TreeStore(tmp_path)
    store.validate()
    return store


@pytest.fixture()
def turn_client(tree_store: TreeStore) -> Generator[TestClient, None, None]:
    from app.main import app

    app.dependency_overrides[get_store] = lambda: tree_store
    client = TestClient(app, raise_server_exceptions=True)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture()
def commit_client() -> TestClient:
    from app.main import app

    return TestClient(app, raise_server_exceptions=True)


@pytest.fixture()
def plain_client() -> TestClient:
    from app.main import app

    return TestClient(app, raise_server_exceptions=True)

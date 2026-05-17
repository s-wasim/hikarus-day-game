
import pytest
from pydantic import ValidationError

from app.schemas.day import (
    VALID_LEAF_IDS,
    Branch,
    ChunkOption,
    Chunks,
    DayResponse,
    JournalEntry,
    Turn,
)
from app.schemas.state import TraitDeltas


def _make_leaf_themes(themes: list[str]) -> dict[str, str]:
    result: dict[str, str] = {}
    for i, leaf_id in enumerate(sorted(VALID_LEAF_IDS)):
        result[leaf_id] = themes[i % len(themes)]
    return result


def _make_chunks() -> Chunks:
    return Chunks(
        slot_1=[
            ChunkOption(id="a", text="Yes"),
            ChunkOption(id="b", text="No"),
            ChunkOption(id="c", text="Maybe"),
        ],
        slot_2=[
            ChunkOption(id="a", text="I am"),
            ChunkOption(id="b", text="it is"),
            ChunkOption(id="c", text="we go"),
        ],
        slot_3=[
            ChunkOption(id="a", text="here."),
            ChunkOption(id="b", text="there."),
            ChunkOption(id="c", text="nowhere."),
        ],
    )


def _make_branch(themes: list[str], incoming: str | None = None) -> Branch:
    return Branch(
        incoming_theme=incoming,
        ai_message="You… are here?",
        chunks=_make_chunks(),
        leaf_themes=_make_leaf_themes(themes),
    )


def _make_valid_response(themes: list[str] | None = None) -> DayResponse:
    themes = themes or ["open", "afraid", "curious"]
    return DayResponse(
        day=0,
        ai_stage="newborn",
        themes=themes,
        turns=[
            Turn(turn_index=0, branches=[_make_branch(themes)]),
            Turn(
                turn_index=1,
                branches=[_make_branch(themes, incoming=t) for t in themes],
            ),
        ],
        journal_entry=JournalEntry(
            day=0, summary="First contact was brief but real.", themes_observed=themes[:1]
        ),
        trait_deltas=TraitDeltas(),
    )


def test_valid_response_parses() -> None:
    r = _make_valid_response()
    assert r.day == 0
    assert len(r.themes) == 3


def test_leaf_themes_wrong_count() -> None:
    themes = ["open", "afraid", "curious"]
    bad_leaf = _make_leaf_themes(themes)
    bad_leaf.pop(next(iter(bad_leaf)))  # remove one entry
    with pytest.raises(ValidationError, match="39"):
        Branch(
            incoming_theme=None,
            ai_message="Hi",
            chunks=_make_chunks(),
            leaf_themes=bad_leaf,
        )


def test_duplicate_themes_rejected() -> None:
    with pytest.raises(ValidationError, match="unique"):
        _make_valid_response(themes=["open", "open", "afraid"])


def test_leaf_theme_not_in_day_themes() -> None:
    themes = ["open", "afraid", "curious"]
    bad_leaf = _make_leaf_themes(themes)
    first_key = next(iter(bad_leaf))
    bad_leaf[first_key] = "unknown_theme"
    with pytest.raises(ValidationError):
        DayResponse(
            day=0,
            ai_stage="newborn",
            themes=themes,
            turns=[Turn(turn_index=0, branches=[
                Branch(incoming_theme=None, ai_message="Hi",
                       chunks=_make_chunks(), leaf_themes=bad_leaf)
            ])],
            journal_entry=JournalEntry(day=0, summary="Test.", themes_observed=["open"]),
            trait_deltas=TraitDeltas(),
        )


def test_json_schema_is_valid() -> None:
    schema = DayResponse.model_json_schema()
    assert isinstance(schema, dict)
    assert "properties" in schema


def test_valid_leaf_ids_count() -> None:
    assert len(VALID_LEAF_IDS) == 39

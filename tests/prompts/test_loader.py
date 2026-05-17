import pytest

from app.prompts.loader import get_base, get_filler, get_planner, get_stage


def test_get_base_nonempty() -> None:
    assert len(get_base()) > 50


def test_get_stage_day_0() -> None:
    content = get_stage(0)
    assert "newborn" in content.lower() or "day 0" in content.lower()


def test_get_stage_day_7() -> None:
    content = get_stage(7)
    assert len(content) > 50


def test_get_stage_invalid() -> None:
    with pytest.raises(ValueError):
        get_stage(99)


def test_get_planner_nonempty() -> None:
    assert len(get_planner()) > 50


def test_get_filler_nonempty() -> None:
    assert len(get_filler()) > 50


def test_stage_day_2_and_3_same() -> None:
    assert get_stage(2) == get_stage(3)


def test_stage_day_4_and_5_same() -> None:
    assert get_stage(4) == get_stage(5)

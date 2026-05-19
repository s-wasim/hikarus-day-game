from pathlib import Path

import pytest

from app.prompt_engine.builder import PromptBuilder
from app.prompt_engine.loader import PromptLoader, init_loader
from app.schemas.commit import CommitRequest, PickedChoice
from app.schemas.conversation import Message, TurnRequest


class TestPromptLoader:
    def test_loads_base(self, tmp_path: Path) -> None:
        _make_minimal_prompts(tmp_path)
        loader = PromptLoader(tmp_path)
        loader.validate()
        assert "arcade cabinet" in loader.get("base")

    def test_missing_day_file_raises(self, tmp_path: Path) -> None:
        _make_minimal_prompts(tmp_path)
        (tmp_path / "DAY0.md").unlink()
        loader = PromptLoader(tmp_path)
        with pytest.raises(FileNotFoundError):
            loader.validate()

    def test_caches_content(self, tmp_path: Path) -> None:
        _make_minimal_prompts(tmp_path)
        loader = PromptLoader(tmp_path)
        loader.validate()
        content1 = loader.get("base")
        (tmp_path / "base.md").write_text("changed", encoding="utf-8")
        content2 = loader.get("base")
        assert content1 == content2

    def test_empty_day_files_are_valid(self, tmp_path: Path) -> None:
        _make_minimal_prompts(tmp_path)
        loader = PromptLoader(tmp_path)
        loader.validate()
        for i in range(11):
            assert loader.get(f"DAY{i}") == ""


class TestPromptBuilder:
    def test_build_turn_contains_day_in_user(self, tmp_path: Path) -> None:
        _make_minimal_prompts(tmp_path)
        loader = PromptLoader(tmp_path)
        loader.validate()
        builder = PromptBuilder(loader)
        request = TurnRequest(day=3)
        system, user = builder.build_turn(request)
        assert "DAY 3" in user
        assert "arcade cabinet" in system

    def test_build_turn_day_stage_only_in_system(self, tmp_path: Path) -> None:
        _make_minimal_prompts(tmp_path, day0_content="UNIQUE_DAY_CONSTRAINT")
        loader = PromptLoader(tmp_path)
        loader.validate()
        builder = PromptBuilder(loader)
        request = TurnRequest(day=0)
        system, user = builder.build_turn(request)
        assert "UNIQUE_DAY_CONSTRAINT" in system
        assert "UNIQUE_DAY_CONSTRAINT" not in user

    def test_build_turn_embeds_summary(self, tmp_path: Path) -> None:
        _make_minimal_prompts(tmp_path)
        loader = PromptLoader(tmp_path)
        loader.validate()
        builder = PromptBuilder(loader)
        request = TurnRequest(day=0, conversation_summary="Hikaru said hello.")
        _, user = builder.build_turn(request)
        assert "Hikaru said hello." in user

    def test_build_commit_contains_choices(self, tmp_path: Path) -> None:
        _make_minimal_prompts(tmp_path)
        loader = PromptLoader(tmp_path)
        loader.validate()
        builder = PromptBuilder(loader)
        request = CommitRequest(
            day=0,
            prior_messages=[Message(text="You?", choices=["Hikaru."])],
            picked_choices=[
                PickedChoice(message_index=0, choice_index=0, choice_text="Hikaru.")
            ],
        )
        _, user = builder.build_commit(request)
        assert "Hikaru." in user


def _make_minimal_prompts(path: Path, day0_content: str = "") -> None:
    (path / "base.md").write_text("You are an AI trapped in an arcade cabinet.", encoding="utf-8")
    (path / "turn_task.md").write_text(
        "DAY {day}\n{hikaru_journal}\n{ai_journal}\n{summary}",
        encoding="utf-8",
    )
    (path / "commit_task.md").write_text(
        "DAY {day}\n{hikaru_journal}\n{ai_journal}\n"
        "{summary}\n{prior_messages}\n{picked_choices}",
        encoding="utf-8",
    )
    (path / "DAY0.md").write_text(day0_content, encoding="utf-8")
    for i in range(1, 11):
        (path / f"DAY{i}.md").write_text("", encoding="utf-8")

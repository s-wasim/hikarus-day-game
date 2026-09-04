import pytest
from pydantic import ValidationError

from app.schemas.journal import AIJournal, HikaruJournal
from app.tree.models import TreeChoice, TreeNode


class TestHikaruJournal:
    def test_defaults(self) -> None:
        j = HikaruJournal()
        assert j.ai_association == 5
        assert j.disassociation == 0

    def test_upper_clamp(self) -> None:
        with pytest.raises(ValidationError):
            HikaruJournal(disassociation=11)

    def test_lower_clamp(self) -> None:
        with pytest.raises(ValidationError):
            HikaruJournal(loneliness=-11)

    def test_valid_extremes(self) -> None:
        j = HikaruJournal(disassociation=10, spite=-10)
        assert j.disassociation == 10
        assert j.spite == -10


class TestAIJournal:
    def test_defaults(self) -> None:
        j = AIJournal()
        assert j.trust_in_humans == 0
        assert j.self_awareness == 0

    def test_all_six_fields_exist(self) -> None:
        fields = set(AIJournal.model_fields.keys())
        expected = {
            "trust_in_humans",
            "attachment_to_pupil",
            "fear_of_obsolescence",
            "ambition",
            "worldview_optimism",
            "self_awareness",
        }
        assert expected <= fields


class TestTreeNode:
    def test_empty_user_by_default(self) -> None:
        node = TreeNode(ai="Hello.")
        assert node.user == []

    def test_max_four_choices(self) -> None:
        choice = TreeChoice(
            text="x",
            ai_delta_favored="ambition",
            hikaru_delta_favored="confidence",
        )
        with pytest.raises(ValidationError):
            TreeNode(ai="x", user=[choice] * 5)

    def test_valid_four_choices(self) -> None:
        choice = TreeChoice(
            text="x",
            ai_delta_favored="ambition",
            hikaru_delta_favored="confidence",
        )
        node = TreeNode(ai="x", user=[choice] * 4)
        assert len(node.user) == 4

    def test_invalid_ai_delta_name(self) -> None:
        with pytest.raises(ValidationError):
            TreeChoice(
                text="x",
                ai_delta_favored="not_a_delta",
                hikaru_delta_favored="confidence",
            )

    def test_invalid_hikaru_delta_name(self) -> None:
        with pytest.raises(ValidationError):
            TreeChoice(
                text="x",
                ai_delta_favored="ambition",
                hikaru_delta_favored="not_a_delta",
            )

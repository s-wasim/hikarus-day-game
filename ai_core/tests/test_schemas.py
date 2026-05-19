import pytest
from pydantic import ValidationError

from app.schemas.commit import CommitRequest, CommitResponse, PickedChoice
from app.schemas.conversation import Message, TurnRequest, TurnResponse
from app.schemas.journal import AIJournal, HikaruJournal


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
        j = AIJournal()
        fields = AIJournal.model_fields.keys()
        expected = {
            "trust_in_humans",
            "attachment_to_pupil",
            "fear_of_obsolescence",
            "ambition",
            "worldview_optimism",
            "self_awareness",
        }
        assert expected <= set(fields)


class TestMessage:
    def test_no_choices_by_default(self) -> None:
        m = Message(text="...")
        assert m.choices == []

    def test_max_four_choices(self) -> None:
        with pytest.raises(ValidationError):
            Message(text="x", choices=["a", "b", "c", "d", "e"])


class TestTurnResponse:
    def test_requires_at_least_one_choice_message(self) -> None:
        with pytest.raises(ValidationError):
            TurnResponse(
                messages=[
                    Message(text="a"),
                    Message(text="b"),
                    Message(text="c"),
                ]
            )

    def test_valid_response(self) -> None:
        tr = TurnResponse(
            messages=[
                Message(text="a"),
                Message(text="b"),
                Message(text="c", choices=["yes", "no"]),
            ]
        )
        assert len(tr.messages) == 3

    def test_min_three_messages_enforced(self) -> None:
        with pytest.raises(ValidationError):
            TurnResponse(messages=[Message(text="only one", choices=["x"])])

    def test_max_ten_messages_enforced(self) -> None:
        messages = [Message(text=f"msg {i}") for i in range(10)]
        messages[0] = Message(text="msg 0", choices=["x"])
        TurnResponse(messages=messages)

        messages.append(Message(text="eleventh"))
        with pytest.raises(ValidationError):
            TurnResponse(messages=messages)


class TestCommitRequest:
    def test_valid(self) -> None:
        req = CommitRequest(
            day=0,
            prior_messages=[Message(text="You?", choices=["Hikaru."])],
            picked_choices=[PickedChoice(message_index=0, choice_index=0, choice_text="Hikaru.")],
        )
        assert req.day == 0

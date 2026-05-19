from pydantic import BaseModel, Field

from app.schemas.conversation import Message
from app.schemas.journal import AIJournal, HikaruJournal


class PickedChoice(BaseModel):
    message_index: int
    choice_index: int
    choice_text: str


class CommitRequest(BaseModel):
    day: int = Field(ge=0, le=10)
    hikaru_journal: HikaruJournal = Field(default_factory=HikaruJournal)
    ai_journal: AIJournal = Field(default_factory=AIJournal)
    conversation_summary: str = ""
    prior_messages: list[Message]
    picked_choices: list[PickedChoice]


class CommitResponse(BaseModel):
    hikaru_journal: HikaruJournal
    ai_journal: AIJournal
    conversation_summary: str

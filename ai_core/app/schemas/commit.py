from pydantic import BaseModel, Field

from app.schemas.journal import AIJournal, AIDeltaName, HikaruDeltaName, HikaruJournal


class PickedChoice(BaseModel):
    node_id: str
    choice_index: int = Field(ge=0, le=3)
    ai_delta_favored: AIDeltaName
    hikaru_delta_favored: HikaruDeltaName


class CommitRequest(BaseModel):
    day: int = Field(ge=0, le=10)
    hikaru_journal: HikaruJournal = Field(default_factory=HikaruJournal)
    ai_journal: AIJournal = Field(default_factory=AIJournal)
    picked_choices: list[PickedChoice]


class CommitResponse(BaseModel):
    hikaru_journal: HikaruJournal
    ai_journal: AIJournal

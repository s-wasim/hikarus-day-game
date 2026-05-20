from pydantic import BaseModel, Field

from app.schemas.journal import AIJournal, HikaruJournal


class TurnRequest(BaseModel):
    day: int = Field(ge=0, le=10)
    hikaru_journal: HikaruJournal = Field(default_factory=HikaruJournal)
    ai_journal: AIJournal = Field(default_factory=AIJournal)


class TurnResponse(BaseModel):
    file_key: str
    tree: dict

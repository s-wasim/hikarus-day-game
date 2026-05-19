from pydantic import BaseModel, Field, model_validator

from app.schemas.journal import AIJournal, HikaruJournal


class Message(BaseModel):
    text: str
    choices: list[str] = Field(default_factory=list, max_length=4)


class TurnRequest(BaseModel):
    day: int = Field(ge=0, le=10)
    hikaru_journal: HikaruJournal = Field(default_factory=HikaruJournal)
    ai_journal: AIJournal = Field(default_factory=AIJournal)
    conversation_summary: str = ""


class TurnResponse(BaseModel):
    messages: list[Message] = Field(min_length=3, max_length=10)

    @model_validator(mode="after")
    def require_at_least_one_choice_message(self) -> "TurnResponse":
        has_choices = any(len(m.choices) > 0 for m in self.messages)
        if not has_choices:
            raise ValueError("At least one message must have choices for the player to pick from")
        return self

from pydantic import BaseModel, Field, field_validator


class DayPlan(BaseModel):
    turn_count: int = Field(ge=2, le=8)
    themes: list[str] = Field(min_length=3, max_length=5)
    beats: list[str] = Field(min_length=1)

    @field_validator("themes")
    @classmethod
    def themes_unique_nonempty(cls, v: list[str]) -> list[str]:
        if len(v) != len(set(v)):
            raise ValueError("themes must be unique")
        if any(not t.strip() for t in v):
            raise ValueError("themes must be non-empty")
        return v

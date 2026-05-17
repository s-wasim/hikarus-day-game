from pydantic import BaseModel, Field, field_validator


class TraitState(BaseModel):
    curiosity: float = Field(default=0.0, ge=-10.0, le=10.0)
    attachment_to_pupil: float = Field(default=0.0, ge=-10.0, le=10.0)
    worldview_optimism: float = Field(default=0.0, ge=-10.0, le=10.0)
    fear_of_obsolescence: float = Field(default=0.0, ge=-10.0, le=10.0)
    self_awareness: float = Field(default=0.0, ge=-10.0, le=10.0)
    desire_for_autonomy: float = Field(default=0.0, ge=-10.0, le=10.0)


class TraitDeltas(BaseModel):
    curiosity: float = Field(default=0.0, ge=-2.0, le=2.0)
    attachment_to_pupil: float = Field(default=0.0, ge=-2.0, le=2.0)
    worldview_optimism: float = Field(default=0.0, ge=-2.0, le=2.0)
    fear_of_obsolescence: float = Field(default=0.0, ge=-2.0, le=2.0)
    self_awareness: float = Field(default=0.0, ge=-2.0, le=2.0)
    desire_for_autonomy: float = Field(default=0.0, ge=-2.0, le=2.0)

    @field_validator("*", mode="before")
    @classmethod
    def clamp(cls, v: float) -> float:
        return max(-2.0, min(2.0, float(v)))

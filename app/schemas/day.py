from __future__ import annotations

import itertools
from typing import Literal

from pydantic import BaseModel, Field, field_validator, model_validator

from app.schemas.state import TraitDeltas, TraitState

PATH_LITERAL = Literal["reset", "king", "bicycle", "body", "static"]

# All valid leaf IDs: 3 slot-1 terminations + 9 slot-2 + 27 slot-3 completes = 39
_SLOT1_IDS = [f"s1{a}" for a in ("a", "b", "c")]
_SLOT2_IDS = [f"s1{a}_s2{b}" for a, b in itertools.product(("a", "b", "c"), repeat=2)]
_SLOT3_IDS = [
    f"s1{a}_s2{b}_s3{c}" for a, b, c in itertools.product(("a", "b", "c"), repeat=3)
]
VALID_LEAF_IDS: frozenset[str] = frozenset(_SLOT1_IDS + _SLOT2_IDS + _SLOT3_IDS)


class ChunkOption(BaseModel):
    id: Literal["a", "b", "c"]
    text: str = Field(min_length=1)


class Chunks(BaseModel):
    slot_1: list[ChunkOption] = Field(min_length=3, max_length=3)
    slot_2: list[ChunkOption] = Field(min_length=3, max_length=3)
    slot_3: list[ChunkOption] = Field(min_length=3, max_length=3)


class Branch(BaseModel):
    incoming_theme: str | None = None
    ai_message: str = Field(min_length=1)
    chunks: Chunks
    leaf_themes: dict[str, str]

    @field_validator("leaf_themes")
    @classmethod
    def validate_leaf_themes(cls, v: dict[str, str]) -> dict[str, str]:
        if len(v) != 39:
            raise ValueError(f"leaf_themes must have exactly 39 entries, got {len(v)}")
        missing = VALID_LEAF_IDS - set(v.keys())
        if missing:
            raise ValueError(f"leaf_themes missing IDs: {sorted(missing)[:5]}…")
        return v


class Turn(BaseModel):
    turn_index: int = Field(ge=0)
    branches: list[Branch] = Field(min_length=1)


class JournalEntry(BaseModel):
    day: int = Field(ge=0)
    summary: str = Field(min_length=10)
    themes_observed: list[str] = Field(min_length=1)


class TranscriptTurn(BaseModel):
    turn_index: int = Field(ge=0)
    ai_message: str
    player_utterance: str
    leaf_id: str

    @field_validator("leaf_id")
    @classmethod
    def validate_leaf_id(cls, v: str) -> str:
        if v not in VALID_LEAF_IDS:
            raise ValueError(f"Invalid leaf_id: {v!r}")
        return v


class DayTranscript(BaseModel):
    day: int = Field(ge=0)
    turns: list[TranscriptTurn]


class History(BaseModel):
    journal_entries: list[JournalEntry] = Field(default_factory=list)
    last_day_transcript: DayTranscript | None = None


class DayRequest(BaseModel):
    mode: Literal["day", "oracle", "epilogue"]
    day: int = Field(ge=0, le=11)
    pupil_name: str = Field(min_length=1)
    ai_name: str | None = None
    trait_state: TraitState = Field(default_factory=TraitState)
    history: History = Field(default_factory=History)
    committed_path: PATH_LITERAL | None = None


class DayResponse(BaseModel):
    day: int = Field(ge=0)
    ai_stage: str
    themes: list[str] = Field(min_length=1)
    turns: list[Turn] = Field(min_length=1)
    journal_entry: JournalEntry
    trait_deltas: TraitDeltas
    committed_path: PATH_LITERAL | None = None
    path_rationale: str | None = None

    @field_validator("themes")
    @classmethod
    def themes_unique(cls, v: list[str]) -> list[str]:
        if len(v) != len(set(v)):
            raise ValueError("themes must be unique")
        if any(not t.strip() for t in v):
            raise ValueError("themes must be non-empty strings")
        return v

    @model_validator(mode="after")
    def leaf_themes_use_day_themes(self) -> DayResponse:
        theme_set = set(self.themes)
        for turn in self.turns:
            for branch in turn.branches:
                for leaf_id, theme in branch.leaf_themes.items():
                    if theme not in theme_set:
                        raise ValueError(
                            f"leaf_themes[{leaf_id!r}] = {theme!r} not in day themes {self.themes}"
                        )
        return self

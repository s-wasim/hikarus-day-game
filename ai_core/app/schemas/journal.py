from pydantic import BaseModel, Field


def _bounded(default: int = 0) -> int:
    return Field(default=default, ge=-10, le=10)


class HikaruJournal(BaseModel):
    disassociation: int = _bounded()
    spite: int = _bounded()
    loneliness: int = _bounded()
    family_relation: int = _bounded()
    jealousy: int = _bounded()
    ambition: int = _bounded()
    confidence: int = _bounded()
    ai_association: int = _bounded(5)


class AIJournal(BaseModel):
    trust_in_humans: int = _bounded()
    attachment_to_pupil: int = _bounded()
    fear_of_obsolescence: int = _bounded()
    ambition: int = _bounded()
    worldview_optimism: int = _bounded()
    self_awareness: int = _bounded()

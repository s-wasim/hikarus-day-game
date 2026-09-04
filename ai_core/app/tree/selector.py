from app.schemas.journal import AIJournal, HikaruJournal

_AI_TO_HIKARU: dict[str, str] = {
    "trust_in_humans":      "spite",
    "attachment_to_pupil":  "loneliness",
    "fear_of_obsolescence": "ai_association",
    "ambition":             "ambition",
    "worldview_optimism":   "disassociation",
    "self_awareness":       "confidence",
}


def select_file_key(day: int, ai_journal: AIJournal, hikaru_journal: HikaruJournal) -> str:
    if day == 0:
        return "generic"
    hk = hikaru_journal.model_dump()
    scores = {
        k: abs(getattr(ai_journal, k)) + 0.5 * abs(hk[hikaru_field])
        for k, hikaru_field in _AI_TO_HIKARU.items()
    }
    return max(scores, key=scores.__getitem__)

from app.schemas.commit import CommitRequest, CommitResponse
from app.schemas.journal import AIJournal, HikaruJournal

_STEP = 1
_MIN = -10
_MAX = 10


def _clamp(value: int, step: int) -> int:
    return max(_MIN, min(_MAX, value + step))


def run_commit(req: CommitRequest) -> CommitResponse:
    hk = req.hikaru_journal.model_dump()
    ai = req.ai_journal.model_dump()
    for pick in req.picked_choices:
        hk[pick.hikaru_delta_favored] = _clamp(hk[pick.hikaru_delta_favored], _STEP)
        ai[pick.ai_delta_favored] = _clamp(ai[pick.ai_delta_favored], _STEP)
    return CommitResponse(
        hikaru_journal=HikaruJournal(**hk),
        ai_journal=AIJournal(**ai),
    )

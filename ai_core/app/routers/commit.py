from fastapi import APIRouter

from app.schemas.commit import CommitRequest, CommitResponse
from app.services.commit import run_commit

router = APIRouter(tags=["commit"])


@router.post("/commit", response_model=CommitResponse)
def commit(request: CommitRequest) -> CommitResponse:
    return run_commit(request)

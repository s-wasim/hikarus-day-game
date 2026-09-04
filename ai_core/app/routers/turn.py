from fastapi import APIRouter, Depends, HTTPException

from app.schemas.conversation import TurnRequest, TurnResponse
from app.services.turn import run_turn
from app.tree.loader import TreeStore, get_store

router = APIRouter(tags=["turn"])


@router.post("/turn", response_model=TurnResponse)
def turn(
    request: TurnRequest,
    store: TreeStore = Depends(get_store),
) -> TurnResponse:
    try:
        return run_turn(request, store)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

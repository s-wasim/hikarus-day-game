from app.schemas.conversation import TurnRequest, TurnResponse
from app.tree.loader import TreeStore
from app.tree.selector import select_file_key


def run_turn(req: TurnRequest, store: TreeStore) -> TurnResponse:
    key = select_file_key(req.day, req.ai_journal, req.hikaru_journal)
    tree = store.load(req.day, key)
    return TurnResponse(file_key=key, tree=tree.root)

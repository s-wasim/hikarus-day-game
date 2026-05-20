from pathlib import Path

from app.tree.models import ConversationTree

_store: "TreeStore | None" = None


class TreeStore:
    def __init__(self, base_dir: Path) -> None:
        self._base_dir = base_dir
        self._cache: dict[tuple[int, str], ConversationTree] = {}

    def validate(self) -> None:
        """Called at startup: ensures base_dir exists and day0/generic.json is present."""
        required = self._base_dir / "day0" / "generic.json"
        if not self._base_dir.exists():
            raise FileNotFoundError(f"turn_configs dir missing: {self._base_dir}")
        if not required.exists():
            raise FileNotFoundError(f"Required boot file missing: {required}")

    def load(self, day: int, file_key: str) -> ConversationTree:
        key = (day, file_key)
        if key not in self._cache:
            path = self._base_dir / f"day{day}" / f"{file_key}.json"
            if not path.exists():
                raise FileNotFoundError(f"No tree file for day={day} key={file_key!r}")
            self._cache[key] = ConversationTree.model_validate_json(path.read_text())
        return self._cache[key]


def init_store(base_dir: Path) -> None:
    global _store
    _store = TreeStore(base_dir)
    _store.validate()


def get_store() -> TreeStore:
    if _store is None:
        raise RuntimeError("TreeStore not initialized")
    return _store

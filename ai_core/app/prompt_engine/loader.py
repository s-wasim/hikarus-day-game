from pathlib import Path

_REQUIRED_NAMES = ["base", "turn_task", "commit_task"] + [f"DAY{i}" for i in range(1)]

_loader: "PromptLoader | None" = None


class PromptLoader:
    def __init__(self, prompts_dir: Path) -> None:
        self._dir = prompts_dir.resolve()
        self._cache: dict[str, str] = {}

    def validate(self) -> None:
        missing = [
            str(self._dir / f"{name}.md")
            for name in _REQUIRED_NAMES
            if not (self._dir / f"{name}.md").exists()
        ]
        if missing:
            raise FileNotFoundError(f"Required prompt files missing: {', '.join(missing)}")
        for name in _REQUIRED_NAMES:
            self.get(name)

    def get(self, name: str) -> str:
        if name not in self._cache:
            path = self._dir / f"{name}.md"
            self._cache[name] = path.read_text(encoding="utf-8")
        return self._cache[name]


def init_loader(prompts_dir: Path) -> PromptLoader:
    global _loader
    _loader = PromptLoader(prompts_dir)
    _loader.validate()
    return _loader


def get_loader() -> PromptLoader:
    if _loader is None:
        raise RuntimeError("PromptLoader not initialized — call init_loader() at startup")
    return _loader

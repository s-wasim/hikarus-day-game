import os

import structlog

from app import config

log = structlog.get_logger()

_STAGE_MAP: dict[int, str] = {
    0: "day_00_newborn.md",
    1: "day_01_naming.md",
    2: "day_02_03_vocabulary.md",
    3: "day_02_03_vocabulary.md",
    4: "day_04_05_sentence_building.md",
    5: "day_04_05_sentence_building.md",
    6: "day_06_07_opinions.md",
    7: "day_06_07_opinions.md",
    8: "day_08_09_self_aware.md",
    9: "day_08_09_self_aware.md",
}

_cache: dict[str, str] = {}


def _load(path: str) -> str:
    if path not in _cache:
        with open(path, encoding="utf-8") as fh:
            _cache[path] = fh.read()
    return _cache[path]


def _prompts_dir() -> str:
    return os.path.abspath(config.PROMPTS_DIR)


def get_base() -> str:
    return _load(os.path.join(_prompts_dir(), "base.md"))


def get_stage(day: int) -> str:
    if day not in _STAGE_MAP:
        raise ValueError(f"No stage prompt for day {day} (days 0-9 supported here)")
    filename = _STAGE_MAP[day]
    return _load(os.path.join(_prompts_dir(), "stages", filename))


def get_planner() -> str:
    return _load(os.path.join(_prompts_dir(), "planner.md"))


def get_filler() -> str:
    return _load(os.path.join(_prompts_dir(), "filler.md"))

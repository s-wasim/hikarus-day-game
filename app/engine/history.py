import structlog

from app.schemas.day import History

log = structlog.get_logger()

_APPROX_CHARS_PER_TOKEN = 4
_WARN_TOKEN_THRESHOLD = 4000


def assemble_history(history: History) -> str:
    parts: list[str] = []

    if history.journal_entries:
        parts.append("=== JOURNAL (past days, summarised) ===")
        for entry in history.journal_entries:
            themes = ", ".join(entry.themes_observed)
            parts.append(f"Day {entry.day} [{themes}]: {entry.summary}")

    if history.last_day_transcript is not None:
        transcript = history.last_day_transcript
        parts.append(f"\n=== YESTERDAY (Day {transcript.day}, full transcript) ===")
        for turn in transcript.turns:
            parts.append(f"[Turn {turn.turn_index}]")
            parts.append(f"  AI: {turn.ai_message}")
            parts.append(f"  Player: {turn.player_utterance}")

    assembled = "\n".join(parts)
    estimated_tokens = len(assembled) // _APPROX_CHARS_PER_TOKEN
    if estimated_tokens > _WARN_TOKEN_THRESHOLD:
        log.warning(
            "history_token_budget_exceeded",
            estimated_tokens=estimated_tokens,
            threshold=_WARN_TOKEN_THRESHOLD,
        )
    else:
        log.debug("history_assembled", estimated_tokens=estimated_tokens)

    return assembled

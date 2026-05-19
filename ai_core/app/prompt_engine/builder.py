from app.prompt_engine.loader import PromptLoader
from app.schemas.commit import CommitRequest
from app.schemas.conversation import TurnRequest


class PromptBuilder:
    def __init__(self, loader: PromptLoader) -> None:
        self._loader = loader

    def build_turn(self, request: TurnRequest) -> tuple[str, str]:
        base = self._loader.get("base")
        day_prompt = self._loader.get(f"DAY{request.day}").strip()

        system = base
        if day_prompt:
            system = f"{base}\n\n{day_prompt}"

        user = self._loader.get("turn_task").format(
            day=request.day,
            hikaru_journal=request.hikaru_journal.model_dump_json(indent=2),
            ai_journal=request.ai_journal.model_dump_json(indent=2),
            summary=request.conversation_summary or "(no prior conversation)",
        )
        return system, user

    def build_commit(self, request: CommitRequest) -> tuple[str, str]:
        base = self._loader.get("base")
        day_prompt = self._loader.get(f"DAY{request.day}").strip()

        system = base
        if day_prompt:
            system = f"{base}\n\n{day_prompt}"

        prior_messages_text = "\n".join(
            f"  [{i}] AI: {m.text}"
            + (
                "\n      Choices offered: " + ", ".join(f'"{c}"' for c in m.choices)
                if m.choices
                else ""
            )
            for i, m in enumerate(request.prior_messages)
        )

        picked_text = "\n".join(
            f"  Message [{p.message_index}] -> Hikaru chose: \"{p.choice_text}\""
            for p in request.picked_choices
        )

        user = self._loader.get("commit_task").format(
            day=request.day,
            hikaru_journal=request.hikaru_journal.model_dump_json(indent=2),
            ai_journal=request.ai_journal.model_dump_json(indent=2),
            summary=request.conversation_summary or "(no prior conversation)",
            prior_messages=prior_messages_text or "(no messages)",
            picked_choices=picked_text or "(no choices made)",
        )
        return system, user

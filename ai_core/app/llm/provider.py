from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class LLMProvider(Protocol):
    async def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: dict[str, Any],
        *,
        max_tokens: int = 2048,
        temperature: float = 0.7,
    ) -> dict[str, Any]: ...

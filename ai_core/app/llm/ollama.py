import asyncio
import json
from typing import Any

import httpx
from httpx import Timeout
import structlog

from app.config import Settings

log = structlog.get_logger()

_MAX_RETRIES = 3
_RETRY_BASE_DELAY = 2.0


class OllamaProvider:
    def __init__(self, settings: Settings) -> None:
        self._base_url = settings.ollama_base_url.rstrip("/")
        self._model = settings.ollama_model
        self._timeout = settings.ollama_timeout_s

    async def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: dict[str, Any],
        *,
        max_tokens: int = 2048,
        temperature: float = 0.3,
    ) -> dict[str, Any]:
        corrective_suffix = ""
        last_error: Exception = RuntimeError("No attempts made")

        for attempt in range(_MAX_RETRIES):
            if attempt > 0:
                delay = _RETRY_BASE_DELAY ** attempt
                log.warning("llm_retry", attempt=attempt, delay=delay)
                await asyncio.sleep(delay)

            try:
                result = await self._call(
                    system_prompt,
                    user_prompt + corrective_suffix,
                    schema,
                    max_tokens,
                    temperature,
                )
                return result
            except (json.JSONDecodeError, ValueError) as e:
                last_error = e
                corrective_suffix = (
                    f"\n\nNote: Your previous output failed JSON parsing: {e}. "
                    "Return only valid JSON matching the schema."
                )
                log.warning("llm_parse_error", attempt=attempt, error=str(e))
            except httpx.HTTPError as e:
                last_error = e
                log.warning("llm_http_error", attempt=attempt, error=str(e))

        raise last_error

    async def _call(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: dict[str, Any],
        max_tokens: int,
        temperature: float,
    ) -> dict[str, Any]:
        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "format": schema,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": max_tokens,
            },
        }

        async with httpx.AsyncClient(timeout=Timeout(self._timeout)) as client:
            response = await client.post(f"{self._base_url}/api/chat", json=payload)
            response.raise_for_status()

        data = response.json()
        content = data["message"]["content"]
        log.debug("llm_response", content_len=len(content))
        return json.loads(content)

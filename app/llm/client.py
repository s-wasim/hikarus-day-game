import asyncio
from typing import Any

import httpx
import structlog

from app import config

log = structlog.get_logger()


class LLMUnavailableError(Exception):
    pass


class OllamaClient:
    def __init__(
        self,
        base_url: str = config.OLLAMA_URL,
        model: str = config.OLLAMA_MODEL,
        timeout: float = config.OLLAMA_TIMEOUT,
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._model = model
        self._timeout = timeout

    async def health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f"{self._base_url}/api/tags")
                return resp.status_code == 200
        except Exception:
            return False

    async def chat(
        self,
        messages: list[dict[str, str]],
        *,
        format: dict[str, Any] | None = None,
        options: dict[str, Any] | None = None,
        temperature: float = 0.8,
    ) -> str:
        payload: dict[str, Any] = {
            "model": self._model,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature, **(options or {})},
        }
        if format is not None:
            payload["format"] = format

        return await self._post_with_retry("/api/chat", payload)

    async def _post_with_retry(self, path: str, payload: dict[str, Any]) -> str:
        url = f"{self._base_url}{path}"
        for attempt in range(2):
            try:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    resp = await client.post(url, json=payload)
                    resp.raise_for_status()
                    data = resp.json()
                    return str(data["message"]["content"])
            except (httpx.ConnectError, httpx.TimeoutException) as exc:
                if attempt == 0:
                    await asyncio.sleep(1)
                    continue
                raise LLMUnavailableError(f"Ollama unreachable at {url}: {exc}") from exc
            except httpx.HTTPStatusError as exc:
                raise LLMUnavailableError(
                    f"Ollama returned {exc.response.status_code}"
                ) from exc
        raise LLMUnavailableError("Ollama unreachable after retry")

from app.config import settings
from app.llm.provider import LLMProvider

_provider: LLMProvider | None = None


def get_provider() -> LLMProvider:
    global _provider
    if _provider is None:
        _provider = _build_provider()
    return _provider


def _build_provider() -> LLMProvider:
    if settings.llm_provider == "ollama":
        from app.llm.ollama import OllamaProvider
        return OllamaProvider(settings)
    raise ValueError(
        f"Unknown LLM_PROVIDER '{settings.llm_provider}'. Supported: 'ollama'."
    )

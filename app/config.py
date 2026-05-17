import os

OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL: str = os.getenv("OLLAMA_MODEL", "qwen2.5:3b-instruct")
OLLAMA_TIMEOUT: float = float(os.getenv("OLLAMA_TIMEOUT", "600"))
PROMPTS_DIR: str = os.path.join(os.path.dirname(__file__), "..", "prompts")

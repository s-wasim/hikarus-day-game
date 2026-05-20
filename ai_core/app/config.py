from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    turn_configs_dir: Path = Path("ai_core/turn_configs")
    log_level: str = "INFO"


settings = Settings()

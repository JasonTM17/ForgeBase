"""Application settings — validated by pydantic at import/boot time."""

from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

AppEnv = Literal["development", "testing", "production"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    """Environment-driven settings.

    A value outside the Literal sets aborts boot with a pydantic
    ValidationError naming the variable — misconfiguration must be loud.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "forgebase-fastapi"
    app_env: AppEnv = "development"
    log_level: LogLevel = "INFO"
    app_port: int = 8000
    # Empty list keeps CORS fully disabled (secure default); origins are
    # provided as a comma-separated list, e.g. CORS_ORIGINS=https://a.com,https://b.com
    cors_origins: list[str] = []


@lru_cache
def get_settings() -> Settings:
    """Cached accessor; dependency-inject in tests via ``Settings(**overrides)``."""
    return Settings()

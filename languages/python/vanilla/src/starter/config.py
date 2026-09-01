"""Environment-driven application configuration with fail-fast validation."""

from __future__ import annotations

import os
from dataclasses import dataclass

VALID_ENVIRONMENTS = ("development", "testing", "production")
VALID_LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


class ConfigError(ValueError):
    """Raised when the environment provides missing or invalid configuration."""


@dataclass(frozen=True)
class AppConfig:
    """Immutable application settings sourced from environment variables."""

    app_name: str
    app_env: str
    log_level: str

    @classmethod
    def from_env(cls, env: dict[str, str] | None = None) -> AppConfig:
        """Build config from ``env`` (defaults to ``os.environ``).

        Validation fails fast here so a misconfigured process never starts
        half-initialized — production config errors must be loud, not latent.
        """
        source = os.environ if env is None else env
        app_name = source.get("APP_NAME", "forgebase-vanilla")
        app_env = source.get("APP_ENV", "development")
        log_level = source.get("LOG_LEVEL", "INFO").upper()

        if not app_name.strip():
            raise ConfigError("APP_NAME must not be empty")
        if app_env not in VALID_ENVIRONMENTS:
            raise ConfigError(f"APP_ENV must be one of {VALID_ENVIRONMENTS}, got {app_env!r}")
        if log_level not in VALID_LOG_LEVELS:
            raise ConfigError(f"LOG_LEVEL must be one of {VALID_LOG_LEVELS}, got {log_level!r}")
        return cls(app_name=app_name, app_env=app_env, log_level=log_level)

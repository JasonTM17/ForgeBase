"""Environment-driven configuration built on Flask's own mechanism.

Flask's ``from_prefixed_env`` loads every ``FORGE_*`` variable; the explicit
``validate()`` pass turns unknown values into a loud boot failure instead of
silently running with bad settings.
"""

from __future__ import annotations

from flask import Flask

VALID_ENVIRONMENTS = ("development", "testing", "production")
VALID_LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


class ConfigError(ValueError):
    """Raised when FORGE_* environment variables are missing or invalid."""


def load_config(app: Flask) -> None:
    """Load FORGE_* environment variables and validate them fail-fast."""
    app.config.from_prefixed_env(prefix="FORGE")
    app_env = app.config.get("APP_ENV", "development")
    log_level = str(app.config.get("LOG_LEVEL", "INFO")).upper()
    if app_env not in VALID_ENVIRONMENTS:
        raise ConfigError(f"FORGE_APP_ENV must be one of {VALID_ENVIRONMENTS}, got {app_env!r}")
    if log_level not in VALID_LOG_LEVELS:
        raise ConfigError(f"FORGE_LOG_LEVEL must be one of {VALID_LOG_LEVELS}, got {log_level!r}")
    app.config["APP_ENV"] = app_env
    app.config["LOG_LEVEL"] = log_level

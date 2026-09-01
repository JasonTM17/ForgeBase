"""Settings validation tests."""

import pytest
from pydantic import ValidationError

from app.core.config import Settings


def test_defaults_are_development_safe():
    settings = Settings()
    assert settings.app_env == "development"
    assert settings.cors_origins == []


def test_invalid_app_env_fails_fast():
    with pytest.raises(ValidationError):
        Settings(app_env="staging")


def test_invalid_log_level_fails_fast():
    with pytest.raises(ValidationError):
        Settings(log_level="verbose")


def test_cors_origins_parse_from_comma_separated_env(monkeypatch):
    monkeypatch.setenv("CORS_ORIGINS", "https://a.com, https://b.com")
    assert Settings().cors_origins == ["https://a.com", "https://b.com"]

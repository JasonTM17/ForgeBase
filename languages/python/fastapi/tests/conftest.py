"""Shared fixtures: isolated app instances per test."""

from __future__ import annotations

import warnings

import pytest
from fastapi.testclient import TestClient

from app.core.config import Settings
from app.main import create_app
from app.services.example_service import ExampleService

warnings.filterwarnings("ignore", category=DeprecationWarning)


@pytest.fixture
def settings() -> Settings:
    return Settings(app_env="testing", cors_origins=[])


@pytest.fixture
def client(settings: Settings, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """Fresh app with a fresh in-memory example store per test."""
    # Patch the reference the route layer actually resolves (examples module).
    monkeypatch.setattr("app.api.routes.examples.example_service", ExampleService())
    return TestClient(create_app(settings))

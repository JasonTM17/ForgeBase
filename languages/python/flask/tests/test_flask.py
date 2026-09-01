"""Health, example flow, error envelope, and config validation tests."""

import pytest

from app import create_app
from app.core.config import ConfigError
from app.services import ExampleService


@pytest.fixture
def client(monkeypatch):
    """Fresh app with a fresh in-memory example store per test."""
    monkeypatch.setattr("app.examples.service", ExampleService())
    app = create_app({"TESTING": True})
    return app.test_client()


def test_health_returns_ok(client):
    assert client.get("/health").get_json() == {"status": "ok"}


def test_liveness_and_readiness_return_ok(client):
    assert client.get("/health/live").get_json() == {"status": "ok"}
    assert client.get("/health/ready").get_json() == {"status": "ok"}


def test_create_returns_envelope(client):
    response = client.post("/api/v1/examples", json={"name": "first"})
    assert response.status_code == 201
    body = response.get_json()
    assert body == {"data": {"id": 1, "name": "first"}, "message": "created"}


def test_get_and_list_flow(client):
    client.post("/api/v1/examples", json={"name": "a"})
    client.post("/api/v1/examples", json={"name": "b"})
    names = [item["name"] for item in client.get("/api/v1/examples").get_json()["data"]]
    assert names == ["a", "b"]
    assert client.get("/api/v1/examples/2").get_json()["data"]["name"] == "b"


def test_unknown_resource_returns_error_envelope(client):
    response = client.get("/api/v1/examples/999")
    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "RESOURCE_NOT_FOUND"


def test_unknown_route_returns_error_envelope(client):
    response = client.get("/api/v1/does-not-exist")
    assert response.status_code == 404
    assert response.get_json()["error"]["code"] == "NOT_FOUND"


def test_blank_name_is_rejected_with_validation_error(client):
    response = client.post("/api/v1/examples", json={"name": ""})
    assert response.status_code == 422
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"


def test_missing_body_is_rejected_with_validation_error(client):
    response = client.post("/api/v1/examples")
    assert response.status_code == 422
    assert response.get_json()["error"]["code"] == "VALIDATION_ERROR"


def test_invalid_app_env_fails_fast(monkeypatch):
    monkeypatch.setenv("FORGE_APP_ENV", "staging")
    with pytest.raises(ConfigError):
        create_app()


def test_invalid_log_level_fails_fast(monkeypatch):
    monkeypatch.setenv("FORGE_LOG_LEVEL", "verbose")
    with pytest.raises(ConfigError):
        create_app()


def test_logging_is_configured_with_json_handler():
    application = create_app()
    handlers = application.logger.handlers
    assert handlers, "app logger must carry the JSON handler"
    assert handlers[0].formatter is not None

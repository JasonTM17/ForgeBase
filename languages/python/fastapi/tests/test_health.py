"""Health contract tests."""


def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_liveness_returns_ok(client):
    assert client.get("/health/live").json() == {"status": "ok"}


def test_readiness_returns_ok(client):
    assert client.get("/health/ready").json() == {"status": "ok"}

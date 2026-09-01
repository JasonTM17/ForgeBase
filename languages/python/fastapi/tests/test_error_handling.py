"""Error envelope contract tests."""


def test_unknown_resource_returns_error_envelope(client):
    response = client.get("/api/v1/examples/999")
    assert response.status_code == 404
    error = response.json()["error"]
    assert error["code"] == "RESOURCE_NOT_FOUND"
    assert "999" in error["message"]


def test_unknown_route_returns_error_envelope(client):
    response = client.get("/api/v1/does-not-exist")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "NOT_FOUND"


def test_validation_error_is_enveloped(client):
    response = client.post("/api/v1/examples", json={})
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "VALIDATION_ERROR"

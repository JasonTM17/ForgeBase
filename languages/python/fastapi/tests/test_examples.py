"""Example resource: the full request -> validation -> service -> envelope flow."""


def test_create_returns_envelope_with_created_item(client):
    response = client.post("/api/v1/examples", json={"name": "first"})
    assert response.status_code == 201
    body = response.json()
    assert body["message"] == "created"
    assert body["data"]["id"] == 1
    assert body["data"]["name"] == "first"


def test_get_returns_created_item(client):
    client.post("/api/v1/examples", json={"name": "first"})
    response = client.get("/api/v1/examples/1")
    assert response.status_code == 200
    assert response.json()["data"]["name"] == "first"


def test_list_returns_all_items(client):
    client.post("/api/v1/examples", json={"name": "a"})
    client.post("/api/v1/examples", json={"name": "b"})
    data = client.get("/api/v1/examples").json()["data"]
    assert [item["name"] for item in data] == ["a", "b"]


def test_blank_name_is_rejected_with_validation_error(client):
    response = client.post("/api/v1/examples", json={"name": ""})
    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "VALIDATION_ERROR"
    assert error["details"]

"""Example resource blueprint demonstrating the full request flow.

Routes only translate HTTP; all business rules live in the service and all
error-to-response mapping happens in the factory's global error handlers.
"""

from __future__ import annotations

from flask import Blueprint, jsonify, request

from app.schemas import ExampleCreate
from app.services import ExampleService

bp = Blueprint("examples", __name__, url_prefix="/api/v1/examples")

# One instance per process; wire a real store behind this interface.
service = ExampleService()


def envelope(data, message: str = "ok"):
    """Success responses are wrapped: {"data": ..., "message": ...}."""
    return jsonify({"data": data, "message": message})


@bp.post("")
def create_example():
    payload = ExampleCreate.model_validate(request.get_json(silent=True) or {})
    created = service.create(payload.name)
    return envelope(created.model_dump(mode="json"), "created"), 201


@bp.get("")
def list_examples():
    return envelope([item.model_dump(mode="json") for item in service.list()])


@bp.get("/<int:item_id>")
def get_example(item_id: int):
    return envelope(service.get(item_id).model_dump(mode="json"))

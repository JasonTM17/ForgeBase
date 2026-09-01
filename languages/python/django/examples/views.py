"""Example resource views demonstrating the Django request flow.

Views only translate HTTP; business rules live in the service and error
mapping happens in common.middleware.ErrorEnvelopeMiddleware.
"""

from __future__ import annotations

import json

from django.http import HttpRequest, HttpResponse, JsonResponse

from examples.schemas import ExampleCreate
from examples.services import service


def envelope(data, message: str = "ok") -> JsonResponse:
    return JsonResponse({"data": data, "message": message})


def examples_collection(request: HttpRequest) -> HttpResponse:
    """GET lists, POST creates — one resource, one URL, dispatched by method."""
    if request.method == "POST":
        return create_example(request)
    return list_examples(request)


def list_examples(request: HttpRequest) -> HttpResponse:
    return envelope([item.model_dump(mode="json") for item in service.list()])


def create_example(request: HttpRequest) -> HttpResponse:
    try:
        data = json.loads(request.body or b"{}")
    except json.JSONDecodeError:
        return JsonResponse(
            {"error": {"code": "VALIDATION_ERROR", "message": "Invalid JSON body"}},
            status=422,
        )
    # Validation errors propagate to the error envelope middleware.
    payload = ExampleCreate.model_validate(data)
    response = envelope(service.create(payload.name).model_dump(mode="json"), "created")
    response.status_code = 201
    return response


def get_example(request: HttpRequest, item_id: int) -> HttpResponse:
    return envelope(service.get(item_id).model_dump(mode="json"))

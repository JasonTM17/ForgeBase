"""Error envelope middleware — the single place errors become JSON responses.

Handles expected domain errors and pydantic validation errors thrown from
any view; framework 404/500 render the same envelope via handler404/500 in
config/urls.py.
"""

from __future__ import annotations

import logging

from django.http import HttpRequest, JsonResponse
from pydantic import ValidationError

from common.exceptions import DomainError

logger = logging.getLogger("app.error")


def json_envelope_response(request: HttpRequest, exception: Exception) -> JsonResponse | None:
    """Map an exception to the error envelope; None lets Django proceed."""
    if isinstance(exception, ValidationError):
        return JsonResponse(
            {
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "details": exception.errors(include_url=False),
                }
            },
            status=422,
        )
    if isinstance(exception, DomainError):
        return JsonResponse(
            {"error": {"code": exception.code, "message": str(exception)}},
            status=exception.status,
        )
    return None


class ErrorEnvelopeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        response = json_envelope_response(request, exception)
        if response is not None:
            return response
        # Unknown exceptions: log server-side, return nothing actionable.
        logger.error("unhandled exception", exc_info=exception)
        return JsonResponse(
            {"error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"}},
            status=500,
        )

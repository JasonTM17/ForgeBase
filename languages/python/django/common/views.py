"""Health views and envelope error handlers."""

from __future__ import annotations

import logging

from django.http import HttpRequest, HttpResponse, JsonResponse

logger = logging.getLogger("app")


def health(request: HttpRequest) -> HttpResponse:
    return JsonResponse({"status": "ok"})


def liveness(request: HttpRequest) -> HttpResponse:
    # The process is running; no dependency checks here by definition.
    return JsonResponse({"status": "ok"})


def readiness(request: HttpRequest) -> HttpResponse:
    # Add dependency probes (database, cache) here as the project grows.
    return JsonResponse({"status": "ok"})


def not_found(request: HttpRequest, exception: Exception) -> HttpResponse:
    return JsonResponse(
        {"error": {"code": "NOT_FOUND", "message": "Resource not found"}}, status=404
    )


def server_error(request: HttpRequest) -> HttpResponse:
    # Details are logged by Django's logging config; never returned to clients.
    logger.error("unhandled server error")
    return JsonResponse(
        {"error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred"}},
        status=500,
    )

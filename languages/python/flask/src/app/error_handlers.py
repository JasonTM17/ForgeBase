"""Global error handlers — the single place errors become HTTP responses.

Every error response follows the envelope:
    {"error": {"code": "...", "message": "..."}}

Production responses never include stack traces or internal details —
unexpected exceptions collapse to a generic 500.
"""

from __future__ import annotations

import logging

from flask import Flask, jsonify
from pydantic import ValidationError
from werkzeug.exceptions import HTTPException

from app.exceptions import DomainError

logger = logging.getLogger("app.error")

# Stable codes for framework-raised HTTP errors clients may branch on.
HTTP_ERROR_CODES = {
    404: "NOT_FOUND",
    405: "METHOD_NOT_ALLOWED",
}


def register_error_handlers(app: Flask) -> None:
    @app.errorhandler(DomainError)
    def domain_error_handler(exc: DomainError):
        # Expected errors are safe to surface verbatim.
        return jsonify({"error": {"code": exc.code, "message": str(exc)}}), exc.status

    @app.errorhandler(ValidationError)
    def validation_error_handler(exc: ValidationError):
        return (
            jsonify(
                {
                    "error": {
                        "code": "VALIDATION_ERROR",
                        "message": "Request validation failed",
                        "details": exc.errors(include_url=False),
                    }
                }
            ),
            422,
        )

    @app.errorhandler(HTTPException)
    def http_exception_handler(exc: HTTPException):
        code = HTTP_ERROR_CODES.get(exc.code, "HTTP_ERROR")
        return jsonify({"error": {"code": code, "message": exc.description}}), exc.code

    @app.errorhandler(Exception)
    def unexpected_error_handler(exc: Exception):
        # Log the full failure server-side; clients get nothing actionable.
        logger.error("unhandled exception", exc_info=exc)
        return (
            jsonify({"error": {"code": "INTERNAL_ERROR",
                               "message": "An unexpected error occurred"}}),
            500,
        )

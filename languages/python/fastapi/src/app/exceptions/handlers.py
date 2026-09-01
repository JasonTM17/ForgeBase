"""Global exception handlers — the single place errors become HTTP responses.

Every response follows the error envelope:
    {"error": {"code": "...", "message": "..."}}

Production responses never include stack traces, database details, or
internal paths — unexpected exceptions collapse to a generic 500.
"""

from __future__ import annotations

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions.base import DomainError

logger = logging.getLogger("app.error")


def _error_body(code: str, message: str, **extra: object) -> dict:
    error: dict = {"code": code, "message": message}
    if extra:
        error.update(extra)
    return {"error": error}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(DomainError)
    async def domain_error_handler(_: Request, exc: DomainError) -> JSONResponse:
        # Expected errors are safe to surface verbatim.
        return JSONResponse(
            status_code=exc.status,
            content=_error_body(exc.code, str(exc)),
        )

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=_error_body(
                "VALIDATION_ERROR",
                "Request validation failed",
                details=exc.errors(),
            ),
        )

    @app.exception_handler(Exception)
    async def unexpected_error_handler(_: Request, exc: Exception) -> JSONResponse:
        # Log the full failure server-side; clients get nothing actionable.
        logger.error("unhandled exception", exc_info=exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=_error_body("INTERNAL_ERROR", "An unexpected error occurred"),
        )

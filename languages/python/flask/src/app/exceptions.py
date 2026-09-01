"""Domain errors raised by services and mapped by global error handlers."""

from __future__ import annotations


class DomainError(Exception):
    """Base class for expected, user-facing errors.

    ``code`` is the stable machine-readable identifier clients can branch on;
    ``status`` is the HTTP status the error handler maps it to.
    """

    code: str = "DOMAIN_ERROR"
    status: int = 400

    def __init__(self, message: str) -> None:
        super().__init__(message)


class NotFoundError(DomainError):
    code = "RESOURCE_NOT_FOUND"
    status = 404


class AlreadyExistsError(DomainError):
    code = "RESOURCE_ALREADY_EXISTS"
    status = 409

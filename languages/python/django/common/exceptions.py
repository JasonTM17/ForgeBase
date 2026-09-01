"""Shared domain errors raised by services, mapped by the error middleware."""

from __future__ import annotations


class DomainError(Exception):
    """Expected, user-facing error mapped by the error envelope middleware.

    ``code`` is the stable machine-readable identifier clients can branch on;
    ``status`` is the HTTP status the middleware maps it to.
    """

    code: str = "DOMAIN_ERROR"
    status: int = 400


class NotFoundError(DomainError):
    code = "RESOURCE_NOT_FOUND"
    status = 404


class AlreadyExistsError(DomainError):
    code = "RESOURCE_ALREADY_EXISTS"
    status = 409

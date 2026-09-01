"""Domain errors raised by services and mapped by the global handlers."""

from app.exceptions.base import AlreadyExistsError, DomainError, NotFoundError
from app.exceptions.handlers import register_exception_handlers

__all__ = [
    "AlreadyExistsError",
    "DomainError",
    "NotFoundError",
    "register_exception_handlers",
]

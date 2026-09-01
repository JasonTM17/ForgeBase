"""Example service demonstrating the testable service layer of the starter."""

from __future__ import annotations


class GreeterService:
    """Greets callers; deliberately trivial, but shaped like real services."""

    def greet(self, name: str) -> str:
        if not name or not name.strip():
            raise ValueError("name must not be empty")
        return f"Hello, {name.strip()}!"

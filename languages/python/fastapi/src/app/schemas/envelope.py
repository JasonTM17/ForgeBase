"""Response envelope shared by all JSON endpoints."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class Envelope[DataT](BaseModel):
    """Success responses are wrapped: {"data": ..., "message": "ok"}."""

    data: DataT
    message: str = "ok"


def envelope(data: Any, message: str = "ok") -> dict:
    """Convenience builder keeping handler code honest and consistent."""
    return {"data": data, "message": message}

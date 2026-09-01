"""Health endpoints following the ForgeBase health contract.

`/health` is the general probe; `/health/live` and `/health/ready` distinguish
liveness (process up, do not restart on failure here) from readiness (able to
serve traffic, e.g. dependencies reachable).
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health/live")
async def liveness() -> dict[str, str]:
    # The process is running; no dependency checks here by definition.
    return {"status": "ok"}


@router.get("/health/ready")
async def readiness() -> dict[str, str]:
    # Add dependency probes (database, cache) here as the project grows.
    return {"status": "ok"}

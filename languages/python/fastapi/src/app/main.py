"""Application factory — the single place the FastAPI app is assembled."""

from __future__ import annotations

from fastapi import FastAPI

from app.api import health


def create_app() -> FastAPI:
    """Build the FastAPI application.

    Kept as a factory (instead of a module-level ``app``) so tests can build
    isolated instances and production can compose settings-driven behavior.
    """
    app = FastAPI(
        title="ForgeBase FastAPI Starter",
        version="1.0.0",
        docs_url="/docs",
        openapi_url="/openapi.json",
    )
    app.include_router(health.router)
    return app


app = create_app()

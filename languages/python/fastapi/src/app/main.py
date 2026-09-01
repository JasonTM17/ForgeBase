"""Application factory — the single place the FastAPI app is assembled."""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import health
from app.core.config import Settings, get_settings
from app.core.logging import setup_logging

logger = logging.getLogger("app")


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build the FastAPI application.

    Accepts injected settings for tests; production reads the environment.
    """
    settings = settings or get_settings()
    setup_logging(settings)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        logger.info("%s starting", settings.app_name)
        yield
        logger.info("%s shutting down", settings.app_name)

    app = FastAPI(
        title="ForgeBase FastAPI Starter",
        version="1.0.0",
        docs_url="/docs",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )
    if settings.cors_origins:
        # Explicit allow-list only; wildcard origins are never implied here.
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
            allow_headers=["Authorization", "Content-Type"],
        )
    app.include_router(health.router)
    return app


app = create_app()

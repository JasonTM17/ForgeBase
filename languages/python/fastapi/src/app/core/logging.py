"""Structured JSON logging, configured once at application creation."""

from __future__ import annotations

import json
import logging
import sys
from datetime import UTC, datetime

from app.core.config import Settings


class JsonFormatter(logging.Formatter):
    """One JSON object per line; uvicorn access/error logs use it too."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def setup_logging(settings: Settings) -> None:
    """Configure root + uvicorn loggers so all output is structured."""
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter())
    # root and uvicorn namespaces share one handler set for uniform output
    for name in ("", "uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(name)
        logger.handlers = [handler]
        logger.propagate = False
        logger.setLevel(settings.log_level)

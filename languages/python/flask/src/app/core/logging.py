"""Structured JSON logging wired into Flask's app logger."""

from __future__ import annotations

import json
import logging
from datetime import UTC, datetime

from flask import Flask


class JsonFormatter(logging.Formatter):
    """One JSON object per line, including Flask request handler errors."""

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


def configure_logging(app: Flask) -> None:
    """Attach the JSON formatter to the app logger at the configured level."""
    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())
    app.logger.handlers = [handler]
    app.logger.propagate = False
    app.logger.setLevel(app.config["LOG_LEVEL"])
    # werkzeug's request logs join the same structured stream.
    werkzeug = logging.getLogger("werkzeug")
    werkzeug.handlers = [handler]
    werkzeug.propagate = False

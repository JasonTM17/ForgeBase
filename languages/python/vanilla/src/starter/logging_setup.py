"""Structured logging setup using only the standard library.

Logs are emitted as one JSON object per line so any log aggregator can parse
them without regexes; human-readable output is a deployment concern, not a
library concern.
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import UTC, datetime

from starter.config import AppConfig


class JsonFormatter(logging.Formatter):
    """Format log records as single-line JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Attach the stack trace only when the caller actually logged an error.
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, ensure_ascii=False)


def configure_logging(config: AppConfig) -> None:
    """Configure the root logger according to the application config.

    Logs go to stderr so stdout stays reserved for program output — a CLI
    piping ``starter World`` must never receive log lines in its pipeline.
    """
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    # Replace default handlers so re-running configure_logging stays idempotent.
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(config.log_level)

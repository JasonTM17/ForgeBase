import json
import logging

from starter.config import AppConfig
from starter.logging_setup import JsonFormatter, configure_logging


def _record(message: str, level: int = logging.INFO) -> logging.LogRecord:
    return logging.LogRecord(
        name="test.logger",
        level=level,
        pathname=__file__,
        lineno=1,
        msg=message,
        args=(),
        exc_info=None,
    )


def test_json_formatter_emits_parseable_json():
    formatted = JsonFormatter().format(_record("hello"))
    payload = json.loads(formatted)
    assert payload["message"] == "hello"
    assert payload["level"] == "INFO"
    assert payload["logger"] == "test.logger"
    assert "timestamp" in payload


def test_configure_logging_sets_level_and_json_handler(capsys):
    config = AppConfig.from_env(env={"LOG_LEVEL": "WARNING"})
    configure_logging(config)
    logging.getLogger("app").warning("watch out")
    output = capsys.readouterr().err.strip()
    assert json.loads(output)["message"] == "watch out"
    # Records below the configured level stay silent.
    logging.getLogger("app").info("quiet")
    assert capsys.readouterr().err == ""


def test_configure_logging_is_idempotent():
    config = AppConfig.from_env(env={})
    configure_logging(config)
    configure_logging(config)
    assert len(logging.getLogger().handlers) == 1

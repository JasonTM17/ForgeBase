"""Bootstrap test: the CLI main() must run end-to-end with valid config."""

import json

from starter.__main__ import main


def test_main_greets_and_returns_success(capsys):
    exit_code = main(["World"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "Hello, World!"
    # The bootstrap log line must be machine-parseable JSON on stderr.
    log_line = next(line for line in captured.err.splitlines() if "application started" in line)
    assert json.loads(log_line)["level"] == "INFO"


def test_main_rejects_invalid_config_without_traceback(capsys, monkeypatch):
    monkeypatch.setenv("APP_ENV", "not-a-real-env")
    exit_code = main(["World"])
    assert exit_code == 1
    assert "configuration error" in capsys.readouterr().err

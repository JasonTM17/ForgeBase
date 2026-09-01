# Python Vanilla Starter

A stdlib-only Python **library/CLI base**: environment-driven configuration,
structured JSON logging, an example service, and a pytest + ruff toolchain.
No runtime dependencies by design — this starter is the foundation layer for
projects that do not need a web framework.

## Features

- Fail-fast, validated configuration from environment variables
- Structured JSON logging (stdlib `logging`, one JSON object per line)
- Example service with unit tests demonstrating the service-layer pattern
- CLI entry point (`python -m starter` / `starter` console script)
- [uv](https://docs.astral.sh/uv/)-managed dev tooling, PEP 621 `pyproject.toml`
- Ruff (lint + format) and pytest preconfigured

## Requirements

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) (or any PEP 621-aware installer)

## Project Structure

```text
vanilla/
├── src/starter/
│   ├── __init__.py        # public exports
│   ├── __main__.py        # CLI entry point
│   ├── config.py          # env-driven config, fail-fast validation
│   ├── logging_setup.py   # JSON logging formatter
│   └── greeter.py         # example service
├── tests/
├── pyproject.toml
└── forgebase.json         # ForgeBase template metadata
```

## Getting Started

Copy this folder out of ForgeBase and rename the package:

```bash
cp -r languages/python/vanilla ~/projects/my-lib
cd ~/projects/my-lib
# rename src/starter -> src/<your_package> and update pyproject.toml
uv sync
```

## Configuration

| Variable   | Default                | Values                                             |
| ---------- | ---------------------- | -------------------------------------------------- |
| `APP_NAME` | `forgebase-vanilla`    | any non-empty string                               |
| `APP_ENV`  | `development`          | `development`, `testing`, `production`             |
| `LOG_LEVEL`| `INFO`                 | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`    |

Invalid values raise `ConfigError` at startup — the process never starts
half-configured. There is intentionally no `.env` loader: this starter has no
runtime dependencies; add `python-dotenv` only if your project needs it.

## Running

```bash
uv run starter World          # console script
uv run python -m starter World
APP_ENV=production LOG_LEVEL=DEBUG uv run starter World
```

## Testing

```bash
uv run pytest
```

## Linting / Formatting

```bash
uv run ruff check .
uv run ruff format --check .
```

## Docker

Deliberately omitted: this is a library/CLI base, not a service. Add a
`Dockerfile` when your project has a runtime shape worth containerizing, or
start from a ForgeBase backend template instead.

## Production Notes

- `LOG_LEVEL=INFO` or higher in production; the JSON formatter is
  aggregator-ready (Loki, Datadog, CloudWatch, ...).
- Configuration is immutable (`frozen` dataclass) — pass `AppConfig` around,
  never raw `os.environ` reads, so behavior stays testable.
- Pin your runtime in CI (`.github/workflows/python.yml` in ForgeBase covers
  this template as a reference).

## Common Issues

- **`uv: command not found`** — install uv (`pip install uv`) or use
  `python -m venv .venv && .venv/bin/pip install -e . pytest ruff` instead.
- **`ModuleNotFoundError: starter`** — run through `uv run`, or
  `pip install -e .` inside your virtualenv.
- **`ConfigError: APP_ENV ...`** — set `APP_ENV` to one of the documented
  values.

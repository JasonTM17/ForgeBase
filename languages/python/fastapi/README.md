# Python FastAPI Starter

A production-oriented **FastAPI REST API base**: validated environment
configuration, structured JSON logging, centralized error handling with a
consistent response envelope, liveness/readiness health endpoints, an example
service demonstrating the router → service → schema flow, and a multi-stage
non-root Docker image.

## Features

- Fail-fast configuration via `pydantic-settings` (validated at startup)
- Structured JSON logging (stdlib `logging`, aggregator-ready)
- Centralized exception handlers — internal errors never leak in production
- Consistent envelope: `{"data": ..., "message": "ok"}` /
  `{"error": {"code", "message"}}`
- `GET /health`, `GET /health/live`, `GET /health/ready`
- Example resource (`/api/v1/examples`) demonstrating request → validation →
  service → response
- CORS configured from environment (empty = disabled)
- pytest + httpx test setup, ruff lint/format, uv-managed dependencies
- Multi-stage Dockerfile (non-root, layer-cached)

## Requirements

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Project Structure

```text
fastapi/
├── src/app/
│   ├── main.py             # application factory
│   ├── api/routes/         # health + example routers
│   ├── core/               # config (pydantic-settings) + logging
│   ├── schemas/            # request/response models + envelope
│   ├── services/           # framework-free business logic
│   └── exceptions/         # domain errors + global handlers
├── tests/
├── pyproject.toml
├── Dockerfile
└── forgebase.json          # ForgeBase template metadata
```

## Getting Started

```bash
cp -r languages/python/fastapi ~/projects/my-api
cd ~/projects/my-api
cp .env.example .env          # then edit values
uv sync
uv run uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs for interactive docs.

## Configuration

Every variable is validated at startup; an invalid value aborts boot with a
clear error.

| Variable        | Default       | Values                                          |
| --------------- | ------------- | ----------------------------------------------- |
| `APP_NAME`      | `forgebase-fastapi` | any non-empty string                      |
| `APP_ENV`       | `development` | `development`, `testing`, `production`          |
| `LOG_LEVEL`     | `INFO`        | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |
| `CORS_ORIGINS`  | *(empty)*     | comma-separated origins, e.g. `https://app.example.com` |

## Running

```bash
uv run uvicorn app.main:app --reload        # development
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2  # production-ish
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

```bash
docker build -t my-api .
docker run --rm -p 8000:8000 --env APP_ENV=production my-api
curl http://localhost:8000/health
```

## Production Notes

- Run behind a reverse proxy (TLS termination, rate limiting) — uvicorn alone
  is not an edge server.
- The example service is in-memory on purpose; swap in your persistence layer
  (SQLAlchemy/…) behind the same service interface.
- Add dependency probes (database, cache) to `/health/ready` as you adopt
  them; keep `/health/live` dependency-free.
- Log output is JSON on stdout/stderr; ship it to your aggregator as-is.

## Common Issues

- **`pydantic-settings` validation error at boot** — an env var has a value
  outside the documented set; the message names the variable.
- **CORS not applied** — `CORS_ORIGINS` is empty by default (secure default);
  set explicit origins.
- **`ModuleNotFoundError: app`** — run through `uv run`, or `pip install -e .`
  in your virtualenv.

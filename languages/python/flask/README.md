# Python Flask Starter

A production-oriented **Flask API base**: application factory, fail-fast
`FORGE_*` environment configuration, structured JSON logging, centralized
error handling with a consistent response envelope, health endpoints, an
example resource demonstrating the blueprint → service flow, and a
multi-stage non-root Docker image.

## Features

- Application-factory pattern (`create_app`) — Flask's recommended structure
- Fail-fast config validation on boot (unknown values abort startup)
- Structured JSON logging for app + werkzeug request logs
- Centralized error handlers — internal errors never leak in production
- Consistent envelope: `{"data": ..., "message": "ok"}` /
  `{"error": {"code", "message"}}`
- `GET /health`, `GET /health/live`, `GET /health/ready`
- Example resource (`/api/v1/examples`) with pydantic input validation
- pytest suite, ruff lint/format, uv-managed dependencies, gunicorn for prod

## Requirements

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Project Structure

```text
flask/
├── src/app/
│   ├── __init__.py        # create_app application factory
│   ├── core/              # config (FORGE_* env) + JSON logging
│   ├── health.py          # health blueprint
│   ├── examples.py        # example resource blueprint
│   ├── services.py        # framework-free business logic
│   ├── schemas.py         # pydantic boundary models
│   ├── exceptions.py      # domain errors
│   └── error_handlers.py  # global error → envelope mapping
├── tests/
├── pyproject.toml
├── Dockerfile
└── forgebase.json         # ForgeBase template metadata
```

## Getting Started

```bash
cp -r languages/python/flask ~/projects/my-api
cd ~/projects/my-api
cp .env.example .env          # then edit values
uv sync
uv run flask --app app run --debug
```

## Configuration

Every `FORGE_*` variable is validated at startup; an invalid value aborts
boot with a clear error.

| Variable          | Default       | Values                                          |
| ----------------- | ------------- | ----------------------------------------------- |
| `FORGE_APP_NAME`  | `forgebase-flask` | any non-empty string                        |
| `FORGE_APP_ENV`   | `development` | `development`, `testing`, `production`          |
| `FORGE_LOG_LEVEL` | `INFO`        | `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL` |

## Running

```bash
uv run flask --app app run --debug                                  # development
uv run gunicorn "app:create_app()" -b 0.0.0.0:8000 -w 2             # production WSGI
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
docker run --rm -p 8000:8000 -e FORGE_APP_ENV=production my-api
curl http://localhost:8000/health
```

## Production Notes

- Gunicorn is included as the production WSGI server; put a reverse proxy
  (TLS, rate limiting) in front of it.
- The example service is in-memory on purpose; swap in your persistence layer
  behind the same interface.
- Add dependency probes to `/health/ready` as you adopt them; keep
  `/health/live` dependency-free.
- Log output is JSON; ship it to your aggregator as-is.

## Common Issues

- **`ConfigError: FORGE_APP_ENV ...`** — the variable has a value outside the
  documented set; fix `.env` or the environment.
- **Routes 404** — make sure you run via the factory
  (`flask --app app run`), not a bare `app.run()` script.
- **`ModuleNotFoundError: app`** — run through `uv run`, or `pip install -e .`
  in your virtualenv.

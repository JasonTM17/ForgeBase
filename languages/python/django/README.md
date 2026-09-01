# Python Django Starter

An **API-only Django base**: environment-driven settings with fail-fast
production checks, structured JSON logging, error envelope middleware, health
endpoints, a generic example app, and a multi-stage non-root Docker image
running gunicorn.

## Features

- Environment-driven `config/settings.py` — invalid/missing production
  settings (`DJANGO_SECRET_KEY`, `FORGE_ALLOWED_HOSTS`) abort boot
- API-only by design: no admin/auth/session apps and no database, so the
  project boots without migrations (add them when you need persistence)
- Structured JSON logging via Django's `LOGGING` dict (app + gunicorn)
- Centralized error envelope: domain errors and validation errors via
  middleware, framework 404/500 via `handler404`/`handler500`
- Consistent envelope: `{"data": ..., "message": "ok"}` /
  `{"error": {"code", "message"}}`
- `GET /health`, `GET /health/live`, `GET /health/ready`
- Example app (`/api/v1/examples`) with pydantic input validation
- Django `manage.py test` suite, ruff lint/format, gunicorn for production

## Requirements

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Project Structure

```text
django/
├── config/            # settings (env-driven), urls, wsgi, asgi, JSON logging
├── common/            # health views, error handlers, domain errors, middleware
├── examples/          # example app: views, urls, schemas, service
├── tests.py           # SimpleTestCase suite (no database needed)
├── manage.py
├── pyproject.toml
├── Dockerfile
└── forgebase.json     # ForgeBase template metadata
```

## Getting Started

```bash
cp -r languages/python/django ~/projects/my-api
cd ~/projects/my-api
cp .env.example .env          # then edit values
uv sync
uv run python manage.py runserver
```

## Configuration

| Variable                | Default                | Notes                                        |
| ----------------------- | ---------------------- | -------------------------------------------- |
| `DJANGO_SECRET_KEY`     | dev-only insecure key  | **required in production** (boot aborts)     |
| `FORGE_APP_ENV`         | `development`          | `development`, `testing`, `production`       |
| `FORGE_LOG_LEVEL`       | `INFO`                 | `DEBUG`…`CRITICAL`                           |
| `FORGE_ALLOWED_HOSTS`   | `localhost,127.0.0.1`  | non-empty **required in production**         |

## Running

```bash
uv run python manage.py runserver                                  # development
uv run gunicorn config.wsgi:application -b 0.0.0.0:8000 -w 2       # production WSGI
```

## Testing

```bash
uv run python manage.py test
```

## Linting / Formatting

```bash
uv run ruff check .
uv run ruff format --check .
```

## Docker

```bash
docker build -t my-api .
docker run --rm -p 8000:8000 \
  -e FORGE_APP_ENV=production \
  -e DJANGO_SECRET_KEY=change-me \
  -e FORGE_ALLOWED_HOSTS=localhost,127.0.0.1 \
  my-api
curl http://localhost:8000/health
```

## Production Notes

- Set a real `DJANGO_SECRET_KEY` (secrets manager, not `.env` files in prod)
  and explicit `FORGE_ALLOWED_HOSTS` — the settings module refuses to boot
  production without them.
- Add `django.contrib` apps + `DATABASES` + migrations when you introduce
  persistence; this starter deliberately ships without them.
- Behind a reverse proxy, pass TLS/rate-limiting concerns to the proxy.

## Common Issues

- **`ImproperlyConfigured: DJANGO_SECRET_KEY is required in production`** —
  set the variable; the starter refuses insecure production boots.
- **DisallowedHost** — add your host to `FORGE_ALLOWED_HOSTS`.
- **Tests fail on imports** — run `uv run python manage.py test` (it wires
  `DJANGO_SETTINGS_MODULE` for you).

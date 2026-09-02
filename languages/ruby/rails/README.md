# Ruby on Rails Starter

A production-oriented Rails 8 API: fail-fast startup configuration,
centralized envelope error handling via `rescue_from`, the health trio,
one example resource, minitest tests, and a non-root Docker image. No
database layer — the example resource uses an in-memory store so the
template stays a clean base (Phase 1 non-goal: DB/ORM).

## Features

- Fail-fast `Forgebase::Config.load_from_environment!` in an initializer —
  the process refuses to boot on a broken configuration
- Centralized envelope errors (`{"error": {"code", "message"}}`) in one
  place (`rescue_from`); production responses never leak stack traces or
  internal details
- Health endpoints: `GET /up` (Rails convention), `/health`, `/health/live`,
  `/health/ready`
- Example resource (`/api/widgets`) demonstrating request -> validation ->
  store -> response with 201/200/204/400/404 semantics
- Gracefully ignores the asset pipeline (API-mode-friendly scaffold)

## Requirements

- Ruby >= 3.3 (verified in the official `ruby:3.3` container image)
- Docker (optional, for containerized runs)

## Project structure

```text
rails/
├── app/
│   ├── controllers/
│   │   ├── application_controller.rb   # rescue_from envelope errors
│   │   └── api/widgets_controller.rb   # example resource
│   └── models/widget.rb                # in-memory store (no DB)
├── config/initializers/forgebase.rb    # fail-fast startup validation
├── config/routes.rb                    # /up, /health trio, /api/widgets
├── lib/forgebase/                      # config, log_severity, console_logger
├── test/controllers/api/widgets_controller_test.rb
└── Dockerfile
```

## Getting started

Copy this folder out and rename:

```bash
cp -r languages/ruby/rails /path/to/my-api
cd /path/to/my-api
# rename the RailsApp module and the forgebase/ namespace
bin/rails db:prepare   # harmless even with no database; creates the schema
bin/rails server
```

## Configuration

| Variable | Required | Default | Meaning |
|---|---|---|---|
| `SERVICE_NAME` | yes | — | service identity used in logs |
| `APP_LOG_LEVEL` | no | `information` | `critical`..`trace` (case-insensitive) |
| `PORT` | no | `3000` | HTTP port Puma binds to |

## Running

```bash
bin/rails server
# then:
curl -s http://localhost:3000/up
curl -s -X POST http://localhost:3000/api/widgets \
  -H "Content-Type: application/json" -d '{"widget":{"name":"anvil"}}'
curl -s http://localhost:3000/api/widgets
```

## Testing

```bash
bin/rails test
```

## Docker

The scaffold's Dockerfile is preserved (multi-stage, non-root). Build and
run:

```bash
docker build -t my-api .
docker run --rm -p 3000:3000 -e SERVICE_NAME=my-api my-api
```

## Production notes

- `rescue_from StandardError` returns a generic message in production to
  avoid leaking internals; override `render_internal` for richer reporting.
- The in-memory widget store is per-process and resets on restart; swap it
  for ActiveRecord when the copied-out project needs persistence.
- `config.autoload_lib` loads `lib/forgebase/*`; keep new library code there.

## Common issues

- **Boot fails with a missing `SERVICE_NAME`** — that is the fail-fast
  contract; set every variable in `.env.example`.
- **Tests reference no database** — run with `RAILS_ENV=test`; the scaffold
  ships an empty `db/schema.rb` for the no-DB case.

# Rust Actix Web Starter

A production-oriented Actix Web 4 API: fail-fast environment configuration,
health endpoints, envelope error responses, an example resource, and a
non-root Docker image. No database layer — the example resource uses an
in-memory store so the template stays a clean base.

## Features

- Fail-fast `Config::from_environment` (clean exit message, code 2)
- Health endpoints: `GET /health`, `GET /health/live`, `GET /health/ready`
- Light response envelope: success is `{"data": ..., "message": "ok"}` and
  errors are `{"error": {"code", "message"}}` via a `ResponseError`
  implementation — no leaked internals
- Example resource (`/api/widgets`) with 201/200/204/400/404 semantics
- Request logging middleware honoring `APP_LOG_LEVEL`
- `actix_web::test` integration tests (no live server)

## Requirements

- Rust stable (verified in the official `rust:1` container image)
- Docker (optional, for containerized runs)

## Project structure

```text
actix-web/
├── Cargo.toml
├── src/
│   ├── lib.rs         # library root (api, config, error, logging)
│   ├── main.rs        # bootstrap: config, shared store, bind
│   ├── api.rs         # routes: health trio + example resource
│   ├── config.rs      # fail-fast environment configuration
│   ├── error.rs       # envelope error contract (ResponseError)
│   └── logging.rs     # leveled UTC-timestamped logging
├── tests/api_test.rs  # integration tests via actix test utilities
├── Dockerfile
└── .env.example
```

## Getting started

Copy this folder out and rename:

```bash
cp -r languages/rust/actix-web /path/to/my-api
cd /path/to/my-api
# rename the crate in Cargo.toml and the binary name
cargo run
```

## Configuration

| Variable | Required | Default | Meaning |
|---|---|---|---|
| `SERVICE_NAME` | yes | — | service identity used in log lines |
| `APP_LOG_LEVEL` | no | `information` | `critical`..`trace` (case-insensitive); also seeds the request-log filter |
| `PORT` | no | `8080` | HTTP port bound on 0.0.0.0 |

## Running

```bash
SERVICE_NAME=demo cargo run
# then:
curl -s http://localhost:8080/health
curl -s -X POST http://localhost:8080/api/widgets \
  -H "Content-Type: application/json" -d '{"name":"anvil"}'
```

## Testing

```bash
cargo test
```

## Linting / formatting

```bash
cargo fmt --check
cargo clippy --all-targets -- -D warnings
```

## Docker

```bash
docker build -t my-api .
docker run --rm -p 8080:8080 -e SERVICE_NAME=my-api my-api
```

Multi-stage build (`rust:1-bookworm` builder → `debian:bookworm-slim`
runtime), non-root system user, only the release binary ships in the image.

## Production notes

- Error responses are built in one place (`error.rs`); add new error
  variants there instead of scattering JSON error maps across handlers.
- The shared widget store lives in one `web::Data` clone per worker;
  swap it for real persistence when the copied-out project needs it.
- Actix performs a graceful shutdown on SIGTERM by default (30s drain);
  tune via `HttpServer::shutdown_timeout` if needed.

## Common issues

- **Port already in use** — set `PORT`; both local runs and the container
  honor it.
- **Path extraction** — extract with `path: Path<u64>` and call
  `into_inner()`; actix's `Path` wrapper has private fields, so pattern
  destructuring does not compile.

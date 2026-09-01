# Rust Axum Starter

A production-oriented Axum 0.8 + Tokio API: fail-fast environment
configuration, health endpoints, envelope error responses, an example
resource, graceful shutdown on SIGTERM/SIGINT, and a non-root Docker image.
No database layer — the example resource uses an in-memory store so the
template stays a clean base.

## Features

- Fail-fast `Config::from_environment` (clean exit message, code 2)
- Health endpoints: `GET /health`, `GET /health/live`, `GET /health/ready`
- Centralized envelope errors: `{"error": {"code", "message"}}` — production
  responses never leak stack traces or internal details
- Example resource (`/api/widgets`) with 201/200/204/400/404 semantics
- Graceful shutdown via `with_graceful_shutdown`
- `tower::ServiceExt::oneshot`-based integration tests (no live server)

## Requirements

- Rust stable (verified in the official `rust:1` container image)
- Docker (optional, for containerized runs)

## Project structure

```text
axum/
├── Cargo.toml
├── src/
│   ├── lib.rs         # library root (api, config, error, logging, shutdown)
│   ├── main.rs        # bootstrap: config, bind, graceful serve
│   ├── api.rs         # router, health trio, example resource
│   ├── config.rs      # fail-fast environment configuration
│   ├── error.rs       # envelope error contract (IntoResponse)
│   ├── logging.rs     # leveled UTC-timestamped logging
│   └── shutdown.rs    # SIGTERM/SIGINT handling
├── tests/api_test.rs  # integration tests via oneshot
├── Dockerfile
└── .env.example
```

## Getting started

Copy this folder out and rename:

```bash
cp -r languages/rust/axum /path/to/my-api
cd /path/to/my-api
# rename the crate in Cargo.toml and the binary name
cargo run
```

## Configuration

| Variable | Required | Default | Meaning |
|---|---|---|---|
| `SERVICE_NAME` | yes | — | service identity used in log lines |
| `APP_LOG_LEVEL` | no | `information` | `critical`..`trace` (case-insensitive) |
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
  variants there instead of scattering `Json` error maps across handlers.
- The in-memory widget store is per-process; swap it for real persistence
  when the copied-out project needs it.
- Logging is a dependency-free module; move to `tracing` + `tower-http`
  when you need spans, structured JSON, or request middleware.

## Common issues

- **Port already in use** — set `PORT`; both local runs and the container
  honor it.
- **Slow first build** — axum compiles a dependency tree; subsequent builds
  reuse `target/`.

# Rust Vanilla Starter

A zero-dependency Rust library/CLI base: fail-fast environment
configuration, leveled logging with ISO-8601 UTC timestamps (standard
library only — no chrono), an example domain service, and integration
tests. `cargo clippy` and `cargo fmt` clean out of the box.

## Features

- Fail-fast `Config::from_environment` with a dedicated `ConfigError`
  (clean exit message instead of a panic)
- Leveled logging via a small `logging` module (errors on stderr, UTC
  timestamps from a civil-from-days formatter)
- Example service with `Result`-based validation errors
- Integration tests through the public API + unit tests per module

## Requirements

- Rust stable (verified in the official `rust:1` container image)

## Project structure

```text
vanilla/
├── Cargo.toml
├── src/
│   ├── lib.rs          # library root (config, logging, greeter modules)
│   ├── config.rs       # fail-fast environment configuration
│   ├── logging.rs      # severity enum + UTC timestamped logger
│   ├── greeter.rs      # example domain service
│   └── main.rs         # CLI demo (clean fail-fast exit)
└── tests/cli_test.rs   # integration tests via the public API
```

## Getting started

Copy this folder out and rename:

```bash
cp -r languages/rust/vanilla /path/to/my-project
cd /path/to/my-project
# rename the crate in Cargo.toml and the module paths
cargo build --release
```

## Configuration

| Variable | Required | Default | Meaning |
|---|---|---|---|
| `SERVICE_NAME` | yes | — | service identity used in log lines |
| `APP_LOG_LEVEL` | no | `information` | one of `critical`, `error`, `warning`, `information`, `debug`, `trace` (case-insensitive) |

Missing or invalid values abort with exit code `2` and a clean message —
no panic, no stack trace.

## Running

```bash
SERVICE_NAME=demo cargo run
```

## Testing

```bash
cargo test
```

## Linting / formatting

```bash
cargo fmt --check
cargo clippy -- -D warnings
```

## Docker

Not applicable: this starter is a library/CLI base with no runtime service.
Repository-level verification runs inside the `rust:1` image; add a
Dockerfile when the copied-out project ships a server component.

## Production notes

- The UTC formatter is standard-library-only; swap in `chrono` or `time`
  when the copied-out project needs richer date handling.
- `LogSeverity` ordering derives from the declaration order — severity
  comparisons stay correct without manual rank methods.
- Configuration errors are values (`Result`), so hosts can map them to
  their own exit semantics.

## Common issues

- **`set_var` warnings after copying out** — the integration tests mutate
  environment variables; on edition 2024 that is `unsafe`. Keep the tests
  on edition 2021 or refactor to inject an env map.

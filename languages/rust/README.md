# Rust Starters

Self-contained Rust basecode templates. Copy a starter folder out of this
repository and it builds as-is — no files outside the folder are referenced.

| Starter | Category | Description |
|---|---|---|
| [`vanilla`](./vanilla/) | library | Zero-dependency library/CLI base: fail-fast env config, leveled logging with UTC timestamps, example service, integration tests |
| [`axum`](./axum/) | backend | Axum + Tokio API: health trio, envelope errors, example resource, graceful shutdown, non-root Docker |
| [`actix-web`](./actix-web/) | backend | Actix Web API: health trio, envelope errors, example resource, non-root Docker |

## Verification strategy

- All starters are verified in the official `rust:1` container
  (`cargo test`, `cargo fmt --check`, `cargo clippy`). No Rust toolchain is
  assumed on the host.
- API starters additionally verify a Docker build of their multi-stage,
  non-root images.

## Copying a starter out

```bash
cp -r languages/rust/axum /path/to/my-api
cd /path/to/my-api
# rename the crate in Cargo.toml and the binary name
cargo build --release
```

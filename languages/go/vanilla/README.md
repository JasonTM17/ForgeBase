# Go Vanilla Starter

Production-oriented **Go library/CLI base** with zero third-party dependencies:
fail-fast environment configuration, structured `slog` logging, a small example
service, and table-driven tests.

## Features

- Go module with idiomatic `cmd/` + `internal/` layout
- Fail-fast `APP_ENV` validation with safe defaults
- Structured JSON logging through the Go standard library `log/slog`
- Example `greeter` service with input validation
- Tests covering config loading and service behavior
- No framework dependency; copy the folder out and it stays independent

## Requirements

- Go >= 1.25

## Project structure

```text
vanilla/
├── cmd/starter/main.go
├── internal/
│   ├── config/config.go
│   └── greeter/greeter.go
├── go.mod
├── .gitignore
└── forgebase.json
```

## Getting started

Copy this folder out and rename the Go module path:

```bash
cp -r languages/go/vanilla /path/to/my-cli
cd /path/to/my-cli
go mod edit -module example.com/my-cli
go test ./...
go run ./cmd/starter ForgeBase
```

## Configuration

| Variable   | Required | Default        | Meaning |
| ---------- | -------- | -------------- | ------- |
| `APP_NAME` | no       | `forgebase-go` | Application/service name used in logs |
| `APP_ENV`  | no       | `development`  | One of `development`, `testing`, `production` |

Invalid `APP_ENV` values return a configuration error before the CLI does work.

## Running

```bash
go run ./cmd/starter ForgeBase
go build -o starter ./cmd/starter
./starter ForgeBase
```

## Testing

```bash
go test ./...
go vet ./...
```

## Linting / formatting

```bash
gofmt -w .
go vet ./...
```

## Docker

Not shipped for this library/CLI starter. Add a Dockerfile in the copied-out
project when you choose a runtime packaging target.

## Production notes

- Keep all environment access behind `internal/config` so invalid runtime
  settings fail early.
- Replace `internal/greeter` with your domain service while preserving the same
  testable boundary.
- Do not commit generated binaries such as `starter.exe`; `.gitignore` excludes
  build outputs.

## Common issues

- **`usage: starter <name>`** — pass a non-empty CLI argument.
- **`configuration error: APP_ENV...`** — set `APP_ENV` to `development`,
  `testing`, or `production`.

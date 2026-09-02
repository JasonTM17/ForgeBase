# Go net/http Starter

A production-oriented **net/http REST base with zero third-party dependencies**:
validated config, structured slog logging, centralized error envelope, health
endpoints, and graceful shutdown.

## Features

- Fail-fast environment configuration (stdlib only)
- Structured JSON logging via `log/slog`
- Consistent envelope: `{"data": ..., "message": "ok"}` /
  `{"error": {"code", "message"}}`
- `GET /health`, `/health/live`, `/health/ready`
- Example resource (`/api/v1/examples`)
- Graceful shutdown on SIGINT/SIGTERM
- **Zero runtime dependencies** — only the Go standard library

## Requirements

- Go >= 1.25

## Project Structure

```text
net-http/
├── cmd/api/                # server entry point + graceful shutdown
├── internal/api/           # HTTP handler + routes
├── internal/config/        # env config + server factory
├── internal/errors/        # error envelope + WriteError
├── internal/examples/      # example service
├── go.mod
└── forgebase.json          # ForgeBase template metadata
```

## Getting Started

```bash
cp -r languages/go/net-http ~/projects/my-api
cd ~/projects/my-api
go mod tidy
go run ./cmd/api
```

## Configuration

| Variable   | Default         | Values                                  |
| ---------- | --------------- | --------------------------------------- |
| `APP_NAME` | `go-net-http`   | any non-empty string                    |
| `APP_ENV`  | `development`   | `development`, `testing`, `production`  |
| `APP_ADDR` | `:8000`         | host:port                               |

## Running

```bash
go run ./cmd/api            # development
go build -o api ./cmd/api && ./api   # production binary
```

## Testing

```bash
go test ./...
```

## Docker

```bash
docker build -t my-api .
docker run --rm -p 8000:8000 -e APP_ENV=production my-api
curl http://localhost:8000/health
```

## Production Notes

- Uses `gcr.io/distroless/static` (non-root, minimal attack surface).
- Structured JSON logs ship to stdout; collect them with your aggregator.
- The example service is in-memory; swap in your persistence layer behind
  the same `examples.Service` interface.

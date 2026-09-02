# Go Fiber Starter

A production-oriented **Fiber v3 REST base**: validated config, structured slog
logging, centralized error envelope, health endpoints, and graceful shutdown.

## Features

- Fail-fast environment configuration
- Structured JSON logging via `log/slog`
- Consistent envelope: `{"data": ..., "message": "ok"}` /
  `{"error": {"code", "message"}}`
- `GET /health`, `/health/live`, `/health/ready`
- Example resource (`/api/v1/examples`)
- Graceful shutdown on SIGINT/SIGTERM

## Requirements

- Go >= 1.25

## Getting Started

```bash
cp -r languages/go/fiber ~/projects/my-api
cd ~/projects/my-api
go mod tidy
go run ./cmd/api
```

## Configuration

| Variable      | Default       | Values                                  |
| ------------- | ------------- | --------------------------------------- |
| `APP_NAME`    | `go-fiber`    | any non-empty string                    |
| `APP_ENV`     | `development` | `development`, `testing`, `production`  |
| `APP_ADDR`    | `:8000`       | host:port                               |
| `CORS_ORIGINS`| *(empty)*     | comma-separated origins                 |

## Testing

```bash
go test ./...
```

## Production Notes

- Distroless runtime (non-root, minimal attack surface).
- Fiber's recovery middleware catches handler panics.

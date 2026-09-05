# Go

Production-oriented Go starters. Each folder is a fully self-contained project.

| Starter  | Category | Description                                         |
| -------- | -------- | --------------------------------------------------- |
| [vanilla](vanilla/) | library | Stdlib-only library/CLI base: env config, slog, go test |
| [net-http](net-http/) | backend | net/http REST base (ZERO third-party deps): error envelope, health, graceful shutdown |
| [gin](gin/) | backend | Gin REST base: slog logging, error envelope, CORS, graceful shutdown |
| [fiber](fiber/) | backend | Fiber v3 REST base: slog logging, explicit CORS allow-list, error envelope, graceful shutdown |

Verification: all templates pass `go test ./...`, `go vet ./...`, and `go build`.

# C# ASP.NET Core Starter

A production-oriented ASP.NET Core 8 minimal API: fail-fast environment
configuration, single-line UTC console logging, RFC 9457 ProblemDetails error
responses, health-check probes, one example resource, and a non-root Docker
image. No database layer — the example resource uses an in-memory store so
the template stays a clean base, not a half-configured application.

## Features

- Fail-fast `EnvConfig`: the process refuses to start on missing or invalid
  environment variables (clean message, exit code 2 — no stack trace)
- Health endpoints: `GET /health`, `GET /health/live`, `GET /health/ready`
  via the health-checks middleware (the ASP.NET Core convention)
- RFC 9457 ProblemDetails for unhandled exceptions, unmatched routes, and
  validation failures — no internal details leak in production responses
- Example resource (`/api/widgets`) demonstrating request → validation →
  store → response with proper 201/204/400/404 semantics
- Graceful-shutdown log hook on application stopping

## Requirements

- .NET SDK 8.0 or newer (verified with SDK 8.0.424)
- Docker (optional, for containerized runs)

## Project structure

```text
aspnetcore/
├── src/Api/
│   ├── Program.cs           # bootstrap: config, logging, health, errors
│   ├── EnvConfig.cs         # fail-fast environment configuration
│   └── WidgetEndpoints.cs   # example resource (in-memory store)
├── tests/Api.Tests/         # WebApplicationFactory integration tests
├── Dockerfile               # multi-stage, non-root
└── .env.example
```

## Getting started

Copy this folder out and rename:

```bash
cp -r languages/csharp/aspnetcore /path/to/my-api
cd /path/to/my-api
# rename the "Api" project/namespace to your product name
dotnet build
dotnet test
```

## Configuration

| Variable | Required | Default | Meaning |
|---|---|---|---|
| `SERVICE_NAME` | yes | — | service identity used in logs |
| `APP_LOG_LEVEL` | no | `Information` | `Trace`..`Critical` (case-insensitive) |
| `PORT` | no | `8080` | HTTP port Kestrel binds to |

## Running

```bash
SERVICE_NAME=demo dotnet run --project src/Api
# then:
curl -s http://localhost:8080/health
curl -s -X POST http://localhost:8080/api/widgets -H "Content-Type: application/json" -d '{"name":"anvil"}'
curl -s http://localhost:8080/api/widgets
```

## Testing

```bash
dotnet test
```

Integration tests use `WebApplicationFactory<Program>` and cover bootstrap,
all three health endpoints, and the widget flow including the
`application/problem+json` 404 shape.

## Linting / formatting

```bash
dotnet format --verify-no-changes
```

## Docker

```bash
docker build -t my-api .
docker run --rm -p 8080:8080 -e SERVICE_NAME=my-api my-api
```

Multi-stage build (`sdk:8.0-alpine` → `aspnet:8.0-alpine`), runs as the
image's non-root `app` user, globalization-invariant for a smaller footprint.

## Production notes

- Error responses never include stack traces or internal details: exceptions
  are mapped by `UseExceptionHandler` + `AddProblemDetails`.
- Configuration is read only from the environment (12-factor); `appsettings`
  exists only as framework plumbing, not as a second config source.
- Swap the in-memory widget store for real persistence when the copied-out
  project needs it — the endpoint layer is store-agnostic by construction.

## Common issues

- **Port already in use** — set `PORT` to a free value; both local runs and
  the Docker image honor it.
- **`InvariantGlobalization`** — enabled for image size; remove the property
  in `Api.csproj` and install ICU libraries if you need culture-specific
  formatting.

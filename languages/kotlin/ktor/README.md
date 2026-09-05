# Kotlin Ktor Starter

A production-oriented Ktor 3 + Netty API: fail-fast environment
configuration, health endpoints, centralized envelope errors via
`StatusPages`, an example resource, content negotiation, and a non-root
Docker image. No database layer — the example resource uses an in-memory
store.

## Features

- Fail-fast `EnvConfig.fromEnvironment` with a dedicated
  `EnvConfigException`
- Health endpoints: `GET /health`, `GET /health/live`, `GET /health/ready`
- Centralized envelope errors (`{"error": {"code", "message"}}`) in one
  place via `StatusPages`; production responses never leak stack traces
- Example resource (`/api/widgets`) with 201/200/204/400/404 semantics
- `kotlin.test` integration tests via Ktor's test host

## Requirements

- JDK 21 (verified in the official `gradle:8.14-jdk21` container image)
- Gradle 8.x (the Kotlin DSL is verified with Gradle 8.14)
- Docker (optional, for containerized runs)

## Project structure

```text
ktor/
├── settings.gradle.kts
├── build.gradle.kts
├── src/
│   ├── main/kotlin/starter/
│   │   ├── ApplicationKt (main + Application.module)
│   │   ├── ApiRoutes.kt     # health trio + example resource
│   │   ├── EnvConfig.kt     # fail-fast environment configuration
│   │   ├── ErrorPages.kt    # StatusPages envelope error handling
│   │   └── LogSeverity.kt   # severity enum + parsing
│   └── test/kotlin/starter/ApiTest.kt
├── Dockerfile
└── .env.example
```

## Getting started

Copy this folder out and rename:

```bash
cp -r languages/kotlin/ktor /path/to/my-api
cd /path/to/my-api
# rename the project in settings.gradle.kts and the starter package
gradle build
```

## Configuration

| Variable | Required | Default | Meaning |
|---|---|---|---|
| `SERVICE_NAME` | yes | — | service identity used in logs |
| `APP_LOG_LEVEL` | no | `information` | `critical`..`trace` (case-insensitive) |
| `PORT` | no | `8080` | HTTP port bound on 0.0.0.0 |

## Running

```bash
SERVICE_NAME=demo gradle run
# then:
curl -s http://localhost:8080/health
curl -s -X POST http://localhost:8080/api/widgets \
  -H "Content-Type: application/json" -d '{"name":"anvil"}'
```

## Testing

```bash
gradle test
```

## Linting / formatting

The starter carries no formatter dependency. Common additions after copying
out: ktlint or Detekt. Sources follow the Kotlin coding conventions.

## Docker

```bash
docker build -t my-api .
docker run --rm -p 8080:8080 -e SERVICE_NAME=my-api my-api
```

Multi-stage build (`gradle:8.14-jdk21` builder → `eclipse-temurin:21-jre-alpine`
runtime), non-root system user, only the release distribution ships in the
image. Verified this session in the official toolchain container:
`gradle test`, the image build, and a boot smoke check (`/health` plus a
widget create).

## Production notes

- Error responses are built in one place (`ErrorPages`); add new exception
  mappings there instead of scattering handlers.
- The in-memory widget store is per-process; swap it for real persistence
  when the copied-out project needs it.
- Add `ktor-server-call-logging` when you need request logs.

## Common issues

- **Port already in use** — set `PORT`; both local runs and the container
  honor it.
- **First build is slow** — Gradle resolves the Ktor dependency tree once;
  subsequent builds reuse `build/`.
- **`gradle` is not installed on the host** — run the repository's documented
  Docker verification command, or generate a Gradle wrapper after copying the
  starter out (`gradle wrapper`).

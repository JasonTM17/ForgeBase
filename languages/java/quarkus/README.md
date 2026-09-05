# Java Quarkus Starter

Production-oriented **Quarkus 3 REST API base**: Java 21, MicroProfile health,
validated environment configuration, centralized REST error mapping, an example
resource, tests, and a fast-jar Docker runtime.

## Features

- Quarkus 3.21 with RESTEasy Reactive / Jackson
- MicroProfile health at `/q/health`, `/q/health/live`, `/q/health/ready`
- Environment-driven application name, environment, and port
- Centralized `ExceptionMapper` for safe error envelopes
- Example resource at `/api/v1/examples`
- Maven build/test workflow and production Dockerfile

## Requirements

- Java 21+
- Maven 3.9+
- Docker 24+ for container builds

## Project structure

```text
quarkus/
├── src/main/java/com/forgebase/quarkus/
│   ├── ExamplesResource.java
│   ├── ExampleService.java
│   ├── GlobalErrorMapper.java
│   └── NotFoundException.java
├── src/main/resources/application.properties
├── src/test/java/com/forgebase/quarkus/
├── .env.example
├── Dockerfile
├── .dockerignore
├── pom.xml
└── forgebase.json
```

## Getting started

Copy this folder out and rename the Maven coordinates/package names:

```bash
cp -r languages/java/quarkus /path/to/my-api
cd /path/to/my-api
mvn quarkus:dev
```

## Configuration

| Variable   | Required | Default             | Meaning |
| ---------- | -------- | ------------------- | ------- |
| `APP_NAME` | no       | `forgebase-quarkus` | Application name |
| `APP_ENV`  | no       | `development`       | Deployment environment label |
| `APP_PORT` | no       | `8000`              | HTTP port |

Quarkus resolves these from the process environment.

## Running

```bash
mvn quarkus:dev
curl http://localhost:8000/q/health
curl http://localhost:8000/q/health/live
curl http://localhost:8000/q/health/ready
```

Production build:

```bash
mvn package
java -jar target/quarkus-app/quarkus-run.jar
```

## Testing

```bash
mvn test
```

The tests cover application bootstrap, MicroProfile health, validation/error
mapping, and the example resource.

## Linting / formatting

No formatter plugin is pinned in this starter. Add Spotless or Checkstyle in the
copied-out service when your team chooses an enforced style profile.

## Docker

```bash
docker build -t my-quarkus-api .
docker run --rm -p 8000:8000 -e APP_ENV=production my-quarkus-api
```

The runtime stage uses a Java 21 JRE image and a non-root `app` user.

## Production notes

- Keep error mapping inside `GlobalErrorMapper` so production responses never
  expose stack traces or internal implementation details.
- Add persistence behind `ExampleService` after copying out; Phase 1 intentionally
  ships no database dependency.
- Tune Quarkus native-image packaging only after your copied-out service needs it.

## Common issues

- **Port already in use** — set `APP_PORT` to a free port.
- **Health endpoint missing** — use `/q/health`; this starter follows Quarkus
  and MicroProfile conventions.

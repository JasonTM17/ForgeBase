# Java Spring Boot Starter

Production-oriented **Spring Boot 3 REST API base**: Java 21, validated
configuration, actuator liveness/readiness probes, RFC 9457 Problem Details,
an example resource, tests, and a non-root Docker image.

## Features

- Spring Boot 3.5 on Java 21
- Environment-driven configuration via `application.yml`
- Actuator health, liveness, and readiness endpoints
- Centralized `@RestControllerAdvice` error mapping with Problem Details
- Example resource at `/api/v1/examples`
- Maven test/build workflow and multi-stage Dockerfile

## Requirements

- Java 21+
- Maven 3.9+
- Docker 24+ for container builds

## Project structure

```text
spring-boot/
├── src/main/java/com/forgebase/springboot/
│   ├── Application.java
│   ├── ExamplesController.java
│   ├── ExampleService.java
│   └── GlobalErrorHandler.java
├── src/main/resources/application.yml
├── src/test/java/com/forgebase/springboot/
├── .env.example
├── Dockerfile
├── .dockerignore
├── pom.xml
└── forgebase.json
```

## Getting started

Copy this folder out and rename the Maven coordinates/package names:

```bash
cp -r languages/java/spring-boot /path/to/my-api
cd /path/to/my-api
cp .env.example .env
mvn spring-boot:run
```

## Configuration

| Variable    | Required | Default            | Meaning |
| ----------- | -------- | ------------------ | ------- |
| `APP_NAME`  | no       | `forgebase-spring` | Spring application name |
| `APP_ENV`   | no       | `development`      | Deployment environment label |
| `APP_PORT`  | no       | `8000`             | HTTP port |
| `LOG_LEVEL` | no       | `INFO`             | Logger level for app package |

Spring imports `.env` when present and also accepts real environment variables.

## Running

```bash
mvn spring-boot:run
curl http://localhost:8000/actuator/health
curl http://localhost:8000/actuator/health/liveness
curl http://localhost:8000/actuator/health/readiness
```

Production build:

```bash
mvn package
java -jar target/*.jar
```

## Testing

```bash
mvn test
```

The tests cover application bootstrap, health probing, validation/error mapping,
and the example resource.

## Linting / formatting

No formatter plugin is pinned in this starter. Add Spotless or Checkstyle in the
copied-out service when your team chooses an enforced style profile.

## Docker

```bash
docker build -t my-spring-api .
docker run --rm -p 8000:8000 -e APP_ENV=production my-spring-api
```

The runtime stage uses a Java 21 JRE image and a non-root `app` user.

## Production notes

- Keep public error responses on the Problem Details path; do not leak stack
  traces or internal exceptions in production responses.
- Add persistence behind `ExampleService` after copying out; Phase 1 intentionally
  ships no database dependency.
- Expose only the actuator endpoints you need in production.

## Common issues

- **Port already in use** — set `APP_PORT` to a free port.
- **Health endpoint missing** — use `/actuator/health`, not `/health`; this
  starter follows Spring Boot's actuator convention.

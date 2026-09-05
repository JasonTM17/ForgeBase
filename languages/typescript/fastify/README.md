# TypeScript Fastify Starter

Production-oriented **Fastify 5 REST API base**: strict TypeScript, zod-validated
configuration, pino structured logging, centralized error envelopes, health
endpoints, an example resource, vitest, and Docker.

## Features

- Fastify 5 with strict TypeScript
- Fail-fast environment validation via zod
- pino JSON logs with configurable level
- Centralized error hook returning safe error envelopes
- `GET /health`, `/health/live`, `/health/ready`
- Example resource under `/api/v1/examples`
- Standard npm scripts: `lint`, `format:check`, `test`, `build`
- Multi-stage Dockerfile with production runtime

## Requirements

- Node.js >= 22
- npm 10+
- Docker 24+ for container builds

## Project structure

```text
fastify/
├── src/
│   ├── config.ts
│   ├── logger.ts
│   ├── plugins/errors.ts
│   ├── routes/
│   ├── services/exampleService.ts
│   └── server.ts
├── test/app.test.ts
├── .env.example
├── Dockerfile
├── .dockerignore
├── package.json
└── forgebase.json
```

## Getting started

Copy this folder out and rename the package:

```bash
cp -r languages/typescript/fastify /path/to/my-api
cd /path/to/my-api
cp .env.example .env
npm install
npm run dev
```

## Configuration

| Variable       | Required | Default             | Meaning                                              |
| -------------- | -------- | ------------------- | ---------------------------------------------------- |
| `APP_NAME`     | no       | `forgebase-fastify` | Service name used in logs/responses                  |
| `APP_ENV`      | no       | `development`       | One of `development`, `testing`, `production`        |
| `LOG_LEVEL`    | no       | `info`              | One of `debug`, `info`, `warn`, `error`              |
| `APP_PORT`     | no       | `3000`              | HTTP port                                            |
| `CORS_ORIGINS` | no       | _(empty)_           | Comma-separated allowed origins; empty disables CORS |

Invalid values throw before the server starts.

## Running

```bash
npm run dev          # tsx watch mode
npm run build
npm run start        # node dist/server.js
```

## Testing

```bash
npm test
```

The tests cover config validation, health endpoints, centralized error handling,
and the example route.

## Linting / formatting

```bash
npm run lint
npm run format:check
```

## Docker

```bash
docker build -t my-fastify-api .
docker run --rm -p 3000:3000 -e APP_ENV=production my-fastify-api
```

## Production notes

- Keep all runtime configuration in `src/config.ts` so boot failures are loud.
- CORS is disabled unless `CORS_ORIGINS` is explicitly set.
- Replace the in-memory example service with your persistence boundary after
  copying out.

## Common issues

- **`Invalid configuration` on boot** — check `.env` values against the table.
- **CORS requests blocked** — set `CORS_ORIGINS` to explicit origins; do not use
  `*` unless your product explicitly allows it.

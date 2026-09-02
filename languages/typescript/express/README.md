# TypeScript Express Starter

A production-oriented **Express 5 REST API base**: zod-validated configuration,
pino structured logging, helmet security headers, centralized error handling
with a consistent envelope, health endpoints, graceful shutdown, and a
non-root Docker image.

## Features

- Fail-fast zod config validation at startup (names the invalid variable)
- pino structured JSON logging with secret redaction (`authorization`, cookies)
- helmet secure headers; CORS only with an explicit allow-list (empty = off)
- Centralized error handler — internal errors never leak in production
- Consistent envelope: `{"data": ..., "message": "ok"}` /
  `{"error": {"code", "message"}}`
- `GET /health`, `GET /health/live`, `GET /health/ready`
- Example resource (`/api/v1/examples`) demonstrating route → service flow
- Graceful shutdown on `SIGTERM`/`SIGINT` (drains in-flight requests)
- vitest + supertest suite, typed ESLint, Prettier

## Requirements

- Node.js >= 22

## Project Structure

```text
express/
├── src/
│   ├── app.ts                  # application factory
│   ├── server.ts               # listen + graceful shutdown
│   ├── config.ts               # zod-validated env config
│   ├── logger.ts               # pino setup with redaction
│   ├── errors.ts               # domain errors
│   ├── routes/                 # health + example routers
│   ├── services/               # framework-free business logic
│   └── middleware/errorHandler.ts
├── test/
├── Dockerfile
└── forgebase.json              # ForgeBase template metadata
```

## Getting Started

```bash
cp -r languages/typescript/express ~/projects/my-api
cd ~/projects/my-api
cp .env.example .env          # then edit values
npm install
npm run dev
```

## Configuration

| Variable       | Default             | Values                                       |
| -------------- | ------------------- | -------------------------------------------- |
| `APP_NAME`     | `forgebase-express` | any non-empty string                         |
| `APP_ENV`      | `development`       | `development`, `testing`, `production`       |
| `LOG_LEVEL`    | `info`              | `debug`, `info`, `warn`, `error`             |
| `APP_PORT`     | `3000`              | 1–65535                                      |
| `CORS_ORIGINS` | _(empty)_           | comma-separated origins; empty disables CORS |

## Running

```bash
npm run dev        # tsx watch, development
npm run build && npm start   # production: node dist/server.js
```

## Testing

```bash
npm test
```

## Linting / Formatting

```bash
npm run lint
npm run format:check
```

## Docker

```bash
docker build -t my-api .
docker run --rm -p 3000:3000 -e APP_ENV=production my-api
curl http://localhost:3000/health
```

## Production Notes

- Run behind a reverse proxy (TLS termination, rate limiting).
- The example service is in-memory on purpose; swap in your persistence layer
  behind the same interface.
- `SIGTERM` triggers graceful shutdown with a 10s drain timeout — tune it to
  your platform's termination grace period.
- Add dependency probes to `/health/ready` as you adopt them.

## Common Issues

- **Boot error naming a variable** — zod rejected an env value; fix `.env`.
- **CORS not applied** — `CORS_ORIGINS` is empty by default (secure default).
- **`Cannot find module`** — run `npm run build` before `npm start`.

# TypeScript NestJS Starter

A production-oriented **NestJS REST API base**: zod-validated configuration
(via `@nestjs/config`), NestJS `Logger`, centralized error handling with a
consistent envelope, Terminus health endpoints, an example module
demonstrating controller → service DI, graceful shutdown, and a non-root
Docker image.

## Features

- Fail-fast zod config validation at startup (names the invalid variable)
- `@nestjs/config` + zod; NestJS `Logger` (swap to pino by preference)
- Centralized exception filter — internal errors never leak in production
- Consistent envelope: `{"data": ..., "message": "ok"}` /
  `{"error": {"code", "message"}}`
- `GET /health` (Terminus), `GET /health/live`, `GET /health/ready`
- Example module (`/api/v1/examples`) demonstrating controller → service DI
- Graceful shutdown (NestJS built-in)
- vitest e2e suite, typed ESLint, Prettier

## Requirements

- Node.js >= 22

## Project Structure

```text
nestjs/
├── src/
│   ├── main.ts               # bootstrap + graceful shutdown
│   ├── app.module.ts         # root module wiring
│   ├── config.ts             # zod-validated env config
│   ├── errors.ts             # domain errors
│   ├── filters/error.filter.ts
│   ├── health/               # Terminus health controller + module
│   └── examples/             # controller, service, module
├── test/app.spec.ts
├── vitest.config.ts
├── package.json
├── tsconfig.json
├── Dockerfile
└── forgebase.json            # ForgeBase template metadata
```

## Getting Started

```bash
cp -r languages/typescript/nestjs ~/projects/my-api
cd ~/projects/my-api
cp .env.example .env          # then edit values
npm install
npm run start:dev
```

## Configuration

| Variable       | Default          | Values                                       |
| -------------- | ---------------- | -------------------------------------------- |
| `APP_NAME`     | `forgebase-nest` | any non-empty string                         |
| `APP_ENV`      | `development`    | `development`, `testing`, `production`       |
| `LOG_LEVEL`    | `info`           | `debug`, `info`, `warn`, `error`             |
| `APP_PORT`     | `3000`           | 1–65535                                      |
| `CORS_ORIGINS` | _(empty)_        | comma-separated origins; empty disables CORS |

## Running

```bash
npm run start:dev    # watch mode, development
npm run start:prod   # node dist/main.js, production
```

## Testing

```bash
npm test             # vitest e2e against the real app
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

- Run behind a reverse proxy (TLS termination, rate limitation).
- The example service is in-memory on purpose; swap in your persistence layer
  behind the same `ExamplesService` interface.
- Add dependency probes to `/health` via Terminus as you adopt them.

## Common Issues

- **Boot error naming a variable** — zod rejected an env value; fix `.env`.
- **Cannot build** — ensure `reflect-metadata` is imported at the top of
  `main.ts` (it is) and `experimentalDecorators` is on in tsconfig.

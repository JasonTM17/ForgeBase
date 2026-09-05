# TypeScript Nuxt Starter

Production-oriented **Nuxt 3 SSR base**: strict TypeScript, typed runtime config,
an idiomatic error page, example page/API route, vitest service tests, and a
node-served Docker image.

## Features

- Nuxt 3 with strict TypeScript
- Public app configuration via Nuxt runtime config
- Example server API at `/api/examples`
- Example page rendering generic items
- Vitest tests for service behavior
- Standard npm scripts: `lint`, `format:check`, `test`, `build`
- Multi-stage Dockerfile running `.output/server/index.mjs`

## Requirements

- Node.js >= 22
- npm 10+
- Docker 24+ for container builds

## Project structure

```text
nuxt/
├── pages/index.vue
├── server/api/
│   ├── examples.get.ts
│   └── service.ts
├── test/app.test.mjs
├── nuxt.config.ts
├── .env.example
├── Dockerfile
├── package.json
└── forgebase.json
```

## Getting started

Copy this folder out and rename the package:

```bash
cp -r languages/typescript/nuxt /path/to/my-app
cd /path/to/my-app
cp .env.example .env
npm install
npm run dev
```

## Configuration

| Variable               | Required | Default | Meaning                                 |
| ---------------------- | -------- | ------- | --------------------------------------- |
| `NUXT_PUBLIC_APP_NAME` | yes      | —       | Public app name available to the client |

Nuxt exposes public runtime configuration to the client and keeps server-only
settings on the server side. Add future runtime config in `nuxt.config.ts`.

## Running

```bash
npm run dev
npm run build
npm run preview
```

## Testing

```bash
npm test
```

The tests cover the example service behavior; add route/component tests after
copying out when you introduce product-specific UI.

## Linting / formatting

```bash
npm run lint
npm run format:check
```

## Docker

```bash
docker build -t my-nuxt-app .
docker run --rm -p 3000:3000 -e NUXT_PUBLIC_APP_NAME=my-app my-nuxt-app
```

The runtime stage serves Nuxt's production output from a Node 22 Alpine image.

## Production notes

- Keep runtime configuration centralized in `nuxt.config.ts`.
- Do not commit `.nuxt/`, `.output/`, `node_modules/`, or generated coverage.
- Add monitoring/error reporting in the copied-out app when you pick a provider.

## Common issues

- **`npm run build` cannot find generated types** — run `npm install`, then rerun
  Nuxt so `.nuxt/` is regenerated locally.
- **Unexpected app name** — confirm `NUXT_PUBLIC_APP_NAME` is present in the
  environment used at build/runtime.

# TypeScript SvelteKit Starter

Production-oriented **SvelteKit 2 SSR base**: Svelte 5, strict TypeScript, typed
`$env/dynamic/public` configuration, idiomatic error route, example page/service,
vitest, and a non-root Node Docker runtime.

## Features

- SvelteKit 2 with Svelte 5 and strict TypeScript
- Typed public config module in `src/lib/config.ts`
- Idiomatic `+error.svelte` error surface
- Example service and server-loaded page
- Vitest tests for config, server load behavior, and service behavior
- Standard npm scripts: `lint`, `format:check`, `test`, `build`
- Multi-stage Dockerfile running adapter-node output as a non-root user

## Requirements

- Node.js >= 22
- npm 10+
- Docker 24+ for container builds

## Project structure

```text
sveltekit/
├── src/
│   ├── lib/
│   │   ├── config.ts
│   │   └── exampleService.ts
│   └── routes/
│       ├── +error.svelte
│       ├── +layout.svelte
│       ├── +page.server.ts
│       └── +page.svelte
├── test/app.test.ts
├── svelte.config.js
├── vite.config.ts
├── vitest.config.ts
├── .env.example
├── Dockerfile
├── package.json
└── forgebase.json
```

## Getting started

Copy this folder out and rename the package:

```bash
cp -r languages/typescript/sveltekit /path/to/my-app
cd /path/to/my-app
cp .env.example .env
npm install
npm run dev
```

## Configuration

| Variable          | Required | Default               | Meaning                                                        |
| ----------------- | -------- | --------------------- | -------------------------------------------------------------- |
| `PUBLIC_APP_NAME` | no       | `forgebase-sveltekit` | Public application name rendered in the page title and heading |

SvelteKit exposes `PUBLIC_*` variables to client code. Keep all environment
access behind `src/lib/config.ts` so invalid values fail during startup/build
instead of being scattered through routes.

## Running

```bash
npm run dev
npm run build
npm run preview
```

The production build uses `@sveltejs/adapter-node` and outputs the Node server
under `.svelte-kit/output`.

## Testing

```bash
npm test
```

The test suite covers config loading, the SvelteKit server load function,
service behavior, and service instance isolation.

## Linting / formatting

```bash
npm run lint
npm run format:check
```

## Docker

```bash
docker build -t my-sveltekit-app .
docker run --rm -p 3000:3000 -e PUBLIC_APP_NAME=my-app my-sveltekit-app
```

The runtime stage uses Node 22 Alpine and drops privileges to an `app` user.

## Production notes

- Keep secrets out of `PUBLIC_*` variables; they are client-visible by design.
- Replace the in-memory example service with your persistence boundary after
  copying out.
- Do not commit `.svelte-kit/`, `build/`, `node_modules/`, or generated coverage.

## Common issues

- **Generated `$types` are missing** — run `npm install` and `npm run build` or
  `npm run dev` so SvelteKit regenerates `.svelte-kit/`.
- **App name did not change** — set `PUBLIC_APP_NAME` in the same environment
  used for build/runtime.

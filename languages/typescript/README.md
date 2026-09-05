# TypeScript

Production-oriented TypeScript starters. Each folder is a fully self-contained
project — copy it out of ForgeBase and start building.

| Starter | Category | Description |
| ------- | -------- | ----------- |
| [node](node/) | library | Zero-dependency TS library/CLI base: strict tsconfig, env config, JSON logging, vitest |
| [express](express/) | backend | Express 5 REST API base: zod config, pino logging, helmet, health endpoints, Docker |
| [nestjs](nestjs/) | backend | NestJS REST API base: config validation, health, centralized filters, Docker |
| [fastify](fastify/) | backend | Fastify 5 REST API base: zod config, pino logging, health endpoints, Docker |
| [react](react/) | frontend | React 19 SPA base: Vite, typed env, error boundary, Testing Library, nginx Docker |
| [nextjs](nextjs/) | frontend | Next.js 15 App Router base: typed public env, error routes, standalone Docker |
| [vue](vue/) | frontend | Vue 3 SPA base: Vite, typed env, app error handler, Vue Test Utils, nginx Docker |
| [nuxt](nuxt/) | frontend | Nuxt 3 SSR base: runtime config, example API/page, vitest, Node Docker |
| [angular](angular/) | frontend | Angular standalone base: typed env, global error handler, vitest, nginx Docker |
| [svelte](svelte/) | frontend | Svelte 5 SPA base: Vite, typed env, example service, vitest, nginx Docker |
| [sveltekit](sveltekit/) | frontend | SvelteKit 2 SSR base: `$env` config, error route, adapter-node Docker |
| [react-native](react-native/) | mobile | Expo React Native base: typed `EXPO_PUBLIC_*` config, error boundary, jest |

## Verification strategy

These templates use the locally-installed Node toolchain (`npm`, TypeScript,
vitest) and, for web-deployable API/frontend starters, Docker builds. React
Native is mobile-oriented: local verification covers typecheck/test/lint, while
native device builds are CI/device-first.

## Copying a starter out

```bash
cp -r languages/typescript/react /path/to/my-app
cd /path/to/my-app
cp .env.example .env
npm install
npm run dev
```

Each starter README documents its exact scripts, environment variables, and
production packaging path.

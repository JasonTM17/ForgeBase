# TypeScript

Production-oriented TypeScript starters. Each folder is a fully self-contained
project — copy it out of ForgeBase and start building.

| Starter | Category | Description |
| ------- | -------- | ----------- |
| [node](node/) | library | Zero-dependency TS library/CLI base: strict tsconfig, env config, JSON logging, vitest |
| [express](express/) | backend | Express 5 REST API base: zod config, pino logging, helmet, health endpoints, Docker |

Verification: these templates are verified with the locally-installed Node
toolchain (npm, vitest, tsc) and — for the API starters — `docker build`.

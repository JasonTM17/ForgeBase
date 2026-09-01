# TypeScript Node Starter

A zero-runtime-dependency **TypeScript library/CLI base**: strict tsconfig,
fail-fast environment configuration, leveled JSON logging, an example service,
and a vitest + ESLint + Prettier toolchain managed by npm.

## Features

- Strict TypeScript (`strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`)
- Fail-fast, validated config from environment variables
- Leveled JSON logging on stderr (stdout reserved for program output)
- Example service with unit tests demonstrating the service-layer pattern
- CLI entry point (`node dist/cli.js` or `npm run build && npm run start`-style)
- Zero runtime dependencies — dev tooling only

## Requirements

- Node.js >= 22

## Project Structure

```text
node/
├── src/
│   ├── index.ts      # library exports
│   ├── cli.ts        # CLI entry point
│   ├── config.ts     # env-driven config, fail-fast validation
│   ├── logger.ts     # leveled JSON logger
│   └── example.ts    # example service
├── test/
├── package.json
├── tsconfig.json
└── forgebase.json    # ForgeBase template metadata
```

## Getting Started

```bash
cp -r languages/typescript/node ~/projects/my-lib
cd ~/projects/my-lib
# rename the package in package.json, then:
npm install
npm run build
```

## Configuration

| Variable    | Default          | Values                                 |
| ----------- | ---------------- | -------------------------------------- |
| `APP_NAME`  | `forgebase-node` | any non-empty string                   |
| `APP_ENV`   | `development`    | `development`, `testing`, `production` |
| `LOG_LEVEL` | `info`           | `debug`, `info`, `warn`, `error`       |

Invalid values throw `ConfigError` at boot. There is intentionally no dotenv
loader: add `dotenv` only if your project needs it.

## Running

```bash
npm run build
node dist/cli.js World
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

Deliberately omitted: this is a library/CLI base, not a service. Add a
`Dockerfile` when your project has a runtime shape worth containerizing.

## Production Notes

- Publish to a registry with `npm publish --access public` (or consume from a
  monorepo); `dist/` carries declarations and source maps.
- Keep runtime dependencies at zero as long as possible; add them only with a
  justification in this README.
- Log output is JSON on stderr; ship it to your aggregator as-is.

## Common Issues

- **`npm test` cannot find modules** — `src` uses ESM (`NodeNext`); import
  paths must end with `.js`.
- **`CONFIGERROR: APP_ENV ...`** — set the variable to one of the documented
  values.

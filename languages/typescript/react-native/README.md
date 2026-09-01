# React Native Starter

An Expo-based React Native starter: typed fail-fast environment
configuration, an app-level error boundary, one example component, jest +
Testing Library tests, and standardized npm scripts. Expo SDK 57, React
19.2, TypeScript 6 in strict mode. No native toolchain required to develop
— Expo Go or a simulator handles the runtime.

## Features

- Typed config module validating `EXPO_PUBLIC_*` variables at load time
  (fail fast on missing values)
- `ErrorBoundary` around the app shell with a recoverable fallback screen
- Example component (`GreetingCard`) with generic-domain content
- jest + `@testing-library/react-native` unit/component tests
- `lint`, `format:check`, `test`, `build` scripts uniform with the other
  TypeScript starters

## Requirements

- Node.js >= 22 (verified with Node 24.12)
- An Expo Go installation or Android/iOS simulator for runtime checks

## Project structure

```text
react-native/
├── App.tsx                     # app shell inside the error boundary
├── src/
│   ├── config.ts               # typed fail-fast environment config
│   ├── components/
│   │   ├── ErrorBoundary.tsx
│   │   └── GreetingCard.tsx    # example component
│   └── __tests__/              # jest + Testing Library tests
├── jest.config.js / jest.setup.ts
├── .env.example
└── app.json                    # Expo app configuration
```

## Getting started

Copy this folder out and rename:

```bash
cp -r languages/typescript/react-native /path/to/my-app
cd /path/to/my-app
npm install
# rename @forgebase/react-native-starter and the app.json identity
npm run start
```

## Configuration

| Variable                   | Required | Default                 | Meaning                                 |
| -------------------------- | -------- | ----------------------- | --------------------------------------- |
| `EXPO_PUBLIC_SERVICE_NAME` | yes      | —                       | service identity shown in the app shell |
| `EXPO_PUBLIC_API_BASE_URL` | no       | `http://localhost:8080` | API base URL for the copied-out project |

Expo inlines `EXPO_PUBLIC_*` variables at bundle time; a missing required
value throws as soon as the config module loads.

## Running

```bash
npm run start          # Metro dev server (scan with Expo Go)
npm run web            # web preview
```

## Testing

```bash
npm test
```

## Linting / formatting

```bash
npm run lint           # eslint with the Expo config
npm run format:check   # prettier
```

## Build

`npm run build` runs the TypeScript compiler in no-emit mode as the local
build gate. Native store builds are deliberately **CI/device-first**:
`eas build` or `npx expo run:[android|ios]` on a machine with the native
toolchain. This repository does not claim local device verification.

## Docker

Not applicable for mobile starters: the verification path is the local
typecheck/test suite plus CI device builds, so no Dockerfile is shipped.

## Production notes

- Move the crash-reporting hook in `ErrorBoundary.componentDidCatch` to
  your real reporting service when copying out.
- Keep all runtime environment access behind `src/config.ts` — Expo only
  inlines `EXPO_PUBLIC_*` variables, and centralizing them keeps the
  contract auditable.
- Run `npx expo prebuild` when you need to eject to bare workflow; the
  generated `ios/`/`android/` directories stay gitignored.

## Common issues

- **`config` throws on startup** — a required `EXPO_PUBLIC_*` variable is
  missing from the environment Expo bundled; check `.env` against
  `.env.example`.
- **Metro cache issues after renaming** — clear with
  `npx expo start --clear`.

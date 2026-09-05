# TypeScript React Starter

A production-oriented **React 19 SPA base**: Vite, strict TypeScript, typed
env config, an error boundary, an example component with a service layer,
and a vitest + Testing Library toolchain served by nginx in Docker.

## Features

- React 19 + Vite 6, strict TypeScript
- Typed env config (VITE_*) with fail-fast validation
- Error boundary — component crashes become a usable UI
- Example component + service demonstrating the service-layer pattern
- vitest + @testing Library, typed ESLint, Prettier
- Standardized scripts: `lint`, `format:check`, `test`, `build`

## Requirements

- Node.js >= 22

## Project Structure

```text
react/
├── src/
│   ├── main.tsx              # React entry point
│   ├── App.tsx               # root component + ErrorBoundary
│   ├── config.ts             # typed env config, fail-fast
│   ├── ErrorBoundary.tsx
│   └── services/             # framework-free business logic
├── test/
├── Dockerfile                # Vite build → nginx serve (SPA fallback)
├── nginx.conf
├── package.json
└── forgebase.json            # ForgeBase template metadata
```

## Getting Started

```bash
cp -r languages/typescript/react ~/projects/my-app
cd ~/projects/my-app
cp .env.example .env
npm install
npm run dev
```

## Configuration

| Variable        | Default           | Notes                |
| --------------- | ----------------- | -------------------- |
| `VITE_APP_NAME` | `forgebase-react` | any non-empty string |

## Running

```bash
npm run dev          # Vite dev server
npm run build && npm run preview   # production build + preview
```

## Testing / Linting

```bash
npm test
npm run lint
npm run format:check
```

## Docker

```bash
docker build -t my-app .
docker run --rm -p 80:80 my-app
```

## Production Notes

- Nginx config ships secure headers and SPA fallback.
- Error boundary logs crashes; wire them to your error tracker.

# TypeScript Angular Starter

Production-oriented **Angular 19 standalone base**: strict TypeScript, typed
env config, global error handler, example component + service, vitest +
Testing Library, and an nginx-served Docker image.

## Quick Start

```bash
cp -r languages/typescript/angular ~/projects/my-app && cd ~/projects/my-app
cp .env.example .env && npm install --legacy-peer-deps && npm run dev
```

## Scripts

`dev` · `build` · `lint` · `format:check` · `test`

## Configuration

| Variable        | Default             |
| --------------- | ------------------- |
| `VITE_APP_NAME` | `forgebase-angular` |

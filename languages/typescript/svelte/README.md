# TypeScript Svelte Starter

Production-oriented **Svelte 5 SPA base**: Vite, strict TypeScript, typed env
config, example component + service (runes), vitest + Testing Library, and an
nginx-served Docker image.

## Quick Start

```bash
cp -r languages/typescript/svelte ~/projects/my-app && cd ~/projects/my-app
cp .env.example .env && npm install --legacy-peer-deps && npm run dev
```

## Scripts

`dev` · `build` · `preview` · `lint` · `format:check` · `test`

## Configuration

| Variable        | Default           |
| --------------- | ----------------- |
| `VITE_APP_NAME` | `forgebase-svelte`|

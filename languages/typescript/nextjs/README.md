# TypeScript Next.js Starter

Production-oriented **Next.js 15 (App Router) base**: strict TypeScript,
zod-validated public env, typed `not-found`, example route + service, vitest +
Testing Library, and a standalone Docker image.

## Quick Start

```bash
cp -r languages/typescript/nextjs ~/projects/my-app && cd ~/projects/my-app
cp .env.example .env && npm install && npm run dev
```

## Scripts

`dev` · `build` · `start` · `lint` · `format:check` · `test`

## Configuration

| Variable               | Required | Default |
| ---------------------- | -------- | ------- |
| `NEXT_PUBLIC_APP_NAME` | yes      | —       |

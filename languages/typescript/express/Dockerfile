# syntax=docker/dockerfile:1
# Multi-stage build: compile TypeScript, prune dev dependencies, slim runtime.

FROM node:22-alpine AS builder

WORKDIR /app
COPY package.json package-lock.json ./
# Lockfile-driven install keeps the dependency tree reproducible.
RUN npm ci
COPY tsconfig.json ./
COPY src ./src
RUN npm run build && npm prune --omit=dev


FROM node:22-alpine AS runtime

ENV NODE_ENV=production

# Non-root runtime user; the app writes nothing to the filesystem.
RUN addgroup -S app && adduser -S app -G app

WORKDIR /app
COPY --from=builder --chown=app:app /app/node_modules ./node_modules
COPY --from=builder --chown=app:app /app/dist ./dist
COPY package.json ./

USER app
EXPOSE 3000

# Healthcheck hits the readiness endpoint shipped with the starter.
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s \
  CMD wget -qO- http://127.0.0.1:3000/health/ready || exit 1

CMD ["node", "dist/server.js"]

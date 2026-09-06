# syntax=docker/dockerfile:1
FROM node:22-alpine AS builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
ARG NEXT_PUBLIC_APP_NAME=forgebase-next
ENV NEXT_PUBLIC_APP_NAME=$NEXT_PUBLIC_APP_NAME
RUN npm run build

FROM node:22-alpine AS runtime
ENV NODE_ENV=production
ARG NEXT_PUBLIC_APP_NAME=forgebase-next
ENV NEXT_PUBLIC_APP_NAME=$NEXT_PUBLIC_APP_NAME
WORKDIR /app
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
EXPOSE 3000
CMD ["node", "server.js"]

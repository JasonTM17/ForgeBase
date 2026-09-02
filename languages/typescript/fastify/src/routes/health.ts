import type { FastifyInstance } from "fastify";

export function healthRoutes(app: FastifyInstance): void {
  app.get("/health", () => ({ status: "ok" }));
  app.get("/health/live", () => ({ status: "ok" }));
  app.get("/health/ready", () => ({ status: "ok" }));
}

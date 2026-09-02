import Fastify, { type FastifyInstance } from "fastify";
import cors from "@fastify/cors";
import { loadConfig } from "./config.js";
import { createLogger } from "./logger.js";
import { registerErrorHook } from "./plugins/errors.js";
import { exampleRoutes } from "./routes/examples.js";
import { healthRoutes } from "./routes/health.js";

export function buildApp(): FastifyInstance {
  const config = loadConfig();
  const app = Fastify({ loggerInstance: createLogger(config) });

  if (config.corsOrigins.length > 0) app.register(cors, { origin: config.corsOrigins });
  registerErrorHook(app);
  app.register(healthRoutes);
  app.register(exampleRoutes);

  app.addHook("onClose", () => app.log.info("shutting down"));
  return app;
}

const config = loadConfig();
const app = buildApp();
void app.listen({ port: config.appPort, host: "0.0.0.0" }).catch((err: unknown) => {
  app.log.error(err, "failed to start");
  process.exit(1);
});

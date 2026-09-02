/**
 * Server entry point with graceful shutdown.
 *
 * SIGTERM/SIGINT stop accepting new connections and wait for in-flight
 * requests to finish — required for clean Kubernetes/container lifecycle.
 */

import { buildApp } from "./app.js";
import { loadConfig } from "./config.js";
import { createLogger } from "./logger.js";

function main(): void {
  const config = loadConfig();
  const logger = createLogger(config);
  const app = buildApp(config, logger);

  const server = app.listen(config.appPort, () => {
    logger.info(`listening on port ${config.appPort}`);
  });

  const shutdown = (signal: string): void => {
    logger.info(`${signal} received — shutting down gracefully`);
    server.close(() => {
      logger.info("server closed");
      process.exit(0);
    });
    // Force-exit if connections do not drain in time.
    setTimeout(() => {
      logger.error("graceful shutdown timed out — forcing exit");
      process.exit(1);
    }, 10_000).unref();
  };

  process.on("SIGTERM", () => shutdown("SIGTERM"));
  process.on("SIGINT", () => shutdown("SIGINT"));
}

main();

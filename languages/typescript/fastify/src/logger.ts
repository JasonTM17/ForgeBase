import pino from "pino";
import type { FastifyBaseLogger } from "fastify";

import type { AppConfig } from "./config.js";

export function createLogger(config: AppConfig): FastifyBaseLogger {
  return pino({
    level: config.logLevel,
    base: { appName: config.appName, appEnv: config.appEnv },
    redact: ["req.headers.authorization", "req.headers.cookie"],
  }) as unknown as FastifyBaseLogger;
}

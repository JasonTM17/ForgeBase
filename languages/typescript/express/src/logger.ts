/**
 * pino logger configured for structured JSON output.
 *
 * pino-pretty is a dev dependency only; production logs are one JSON object
 * per line on stdout, ready for any aggregator.
 */

import pino from "pino";

import type { AppConfig } from "./config.js";

export type Logger = pino.Logger;

export function createLogger(config: AppConfig): Logger {
  return pino({
    level: config.logLevel,
    base: { appName: config.appName, appEnv: config.appEnv },
    // Redact common secret holders by path; extend as the app grows.
    redact: ["req.headers.authorization", "req.headers.cookie"],
  });
}

import { Logger } from "@nestjs/common";

import { loadConfig } from "./config.js";

/**
 * Builds the global NestJS Logger from validated config at boot.
 */
export function createLogger() {
  const config = loadConfig();
  const logger = new Logger(config.appName);
  return { config, logger };
}

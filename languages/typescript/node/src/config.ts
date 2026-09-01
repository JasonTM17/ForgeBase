/**
 * Fail-fast environment configuration.
 *
 * Config problems must stop the process at boot, not surface later as
 * undefined runtime behavior.
 */

export type AppEnv = "development" | "testing" | "production";
export type LogLevel = "debug" | "info" | "warn" | "error";

const VALID_ENVS: readonly AppEnv[] = ["development", "testing", "production"];
const VALID_LEVELS: readonly LogLevel[] = ["debug", "info", "warn", "error"];

export class ConfigError extends Error {}

export interface AppConfig {
  readonly appName: string;
  readonly appEnv: AppEnv;
  readonly logLevel: LogLevel;
}

export function loadConfig(env: Record<string, string | undefined> = process.env): AppConfig {
  const appName = env.APP_NAME ?? "forgebase-node";
  const appEnv = (env.APP_ENV ?? "development") as AppEnv;
  const logLevel = (env.LOG_LEVEL ?? "info").toLowerCase() as LogLevel;

  if (!appName.trim()) {
    throw new ConfigError("APP_NAME must not be empty");
  }
  if (!VALID_ENVS.includes(appEnv)) {
    throw new ConfigError(`APP_ENV must be one of ${VALID_ENVS.join(", ")}, got ${appEnv}`);
  }
  if (!VALID_LEVELS.includes(logLevel)) {
    throw new ConfigError(`LOG_LEVEL must be one of ${VALID_LEVELS.join(", ")}, got ${logLevel}`);
  }
  return { appName, appEnv, logLevel };
}

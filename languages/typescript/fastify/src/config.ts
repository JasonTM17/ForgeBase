import { z } from "zod";

const envSchema = z.object({
  APP_NAME: z.string().min(1).default("forgebase-fastify"),
  APP_ENV: z.enum(["development", "testing", "production"]).default("development"),
  LOG_LEVEL: z.enum(["debug", "info", "warn", "error"]).default("info"),
  APP_PORT: z.coerce.number().int().min(1).max(65535).default(3000),
  CORS_ORIGINS: z
    .string()
    .default("")
    .transform((v) =>
      v
        .split(",")
        .map((o) => o.trim())
        .filter(Boolean),
    ),
});

export interface AppConfig {
  appName: string;
  appEnv: "development" | "testing" | "production";
  logLevel: "debug" | "info" | "warn" | "error";
  appPort: number;
  corsOrigins: string[];
}

export function loadConfig(env: Record<string, string | undefined> = process.env): AppConfig {
  const parsed = envSchema.safeParse(env);
  if (!parsed.success) {
    const details = parsed.error.issues
      .map((i) => `${i.path.join(".") || "env"}: ${i.message}`)
      .join("; ");
    throw new Error(`Invalid configuration — ${details}`);
  }
  const { APP_NAME, APP_ENV, LOG_LEVEL, APP_PORT, CORS_ORIGINS } = parsed.data;
  return {
    appName: APP_NAME,
    appEnv: APP_ENV,
    logLevel: LOG_LEVEL,
    appPort: APP_PORT,
    corsOrigins: CORS_ORIGINS,
  };
}

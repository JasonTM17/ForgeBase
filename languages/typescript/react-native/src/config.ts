// Central typed environment access. Expo inlines EXPO_PUBLIC_* variables at
// bundle time; validation happens at module load so a broken configuration
// fails fast instead of surfacing at runtime.

export interface AppConfig {
  serviceName: string;
  apiBaseUrl: string;
}

function required(
  env: Record<string, string | undefined>,
  name: string,
): string {
  const value = env[name];
  if (value === undefined || value.trim() === "") {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
}

function optional(
  env: Record<string, string | undefined>,
  name: string,
  fallback: string,
): string {
  const value = env[name];
  return value === undefined || value.trim() === "" ? fallback : value;
}

// Exposed separately from `config` so tests can exercise the validation
// contract without manipulating the real environment.
export function loadConfig(env: Record<string, string | undefined>): AppConfig {
  return {
    serviceName: required(env, "EXPO_PUBLIC_SERVICE_NAME"),
    apiBaseUrl: optional(
      env,
      "EXPO_PUBLIC_API_BASE_URL",
      "http://localhost:8080",
    ),
  };
}

export const config: AppConfig = loadConfig(process.env);

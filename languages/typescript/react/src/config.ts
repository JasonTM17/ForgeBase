/// <reference types="vite/client" />

/**
 * Fail-fast, typed environment configuration.
 *
 * Public runtime variables are declared in vite-env.d.ts (VITE_* prefix).
 * Missing/invalid values throw at module load so misconfiguration is loud.
 */

function required(name: keyof ImportMetaEnv, fallback?: string): string {
  const value = import.meta.env[name] ?? fallback;
  if (value === undefined || value.trim() === "") {
    throw new Error(`Missing required env variable: ${name}`);
  }
  return value.trim();
}

export const appName = required("VITE_APP_NAME", "forgebase-react");

/// <reference types="vite/client" />

function required(name: keyof ImportMetaEnv, fallback?: string): string {
  const value = import.meta.env[name] ?? fallback;
  if (value === undefined || value.trim() === "") throw new Error(`Missing required env: ${name}`);
  return value.trim();
}

export const appName = required("VITE_APP_NAME", "forgebase-vue");

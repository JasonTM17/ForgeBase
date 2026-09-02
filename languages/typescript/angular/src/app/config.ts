/// <reference types="vite/client" />

export function required(name: keyof ImportMetaEnv, fallback?: string): string {
  const value = import.meta.env[name] ?? fallback;
  if (value === undefined || value.trim() === "") {
    throw new Error(`Missing required env variable: ${name}`);
  }
  return value.trim();
}

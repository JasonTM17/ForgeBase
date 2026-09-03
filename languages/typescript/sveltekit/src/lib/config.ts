import { env } from "$env/dynamic/public";

function required(name: string, value: string | undefined, fallback?: string): string {
  const resolved = value ?? fallback;
  if (resolved === undefined || resolved.trim() === "") {
    throw new Error(`Missing required env variable: ${name}`);
  }
  return resolved.trim();
}

export const appName = required("PUBLIC_APP_NAME", env.PUBLIC_APP_NAME, "forgebase-sveltekit");

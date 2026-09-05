import { env } from "$env/dynamic/public";

function required(name: string, value: string | undefined): string {
  if (value === undefined || value.trim() === "") {
    throw new Error(`Missing required env variable: ${name}`);
  }
  return value.trim();
}

export const appName = required("PUBLIC_APP_NAME", env.PUBLIC_APP_NAME);

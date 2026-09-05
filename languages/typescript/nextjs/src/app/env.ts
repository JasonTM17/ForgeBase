import { z } from "zod";

/**
 * Fail-fast, zod-validated public environment configuration.
 * Only NEXT_PUBLIC_* variables are exposed to the browser.
 */
const envSchema = z.object({
  NEXT_PUBLIC_APP_NAME: z.string().trim().min(1),
});

const parsed = envSchema.safeParse(process.env);
if (!parsed.success) {
  const details = parsed.error.issues.map((i) => `${i.path.join(".")}: ${i.message}`).join("; ");
  throw new Error(`Invalid public env — ${details}`);
}

export const { NEXT_PUBLIC_APP_NAME: appName } = parsed.data;

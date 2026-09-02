// Vitest config for the NestJS starter (unit + e2e share one config).
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["test/**/*.spec.ts"],
    globals: true,
  },
});

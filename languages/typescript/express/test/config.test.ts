import { describe, expect, it } from "vitest";

import { loadConfig } from "../src/config.js";

describe("loadConfig", () => {
  it("defaults to development-safe values", () => {
    const config = loadConfig({});
    expect(config).toMatchObject({ appEnv: "development", logLevel: "info", corsOrigins: [] });
  });

  it("parses comma-separated CORS origins", () => {
    expect(loadConfig({ CORS_ORIGINS: "https://a.com, https://b.com" }).corsOrigins).toEqual([
      "https://a.com",
      "https://b.com",
    ]);
  });

  it("fails fast naming the invalid variable", () => {
    expect(() => loadConfig({ APP_ENV: "staging" })).toThrow(/APP_ENV/);
    expect(() => loadConfig({ APP_PORT: "not-a-port" })).toThrow(/APP_PORT/);
  });
});

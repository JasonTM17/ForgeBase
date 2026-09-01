import { describe, expect, it } from "vitest";

import { ConfigError, loadConfig } from "../src/config.js";

describe("loadConfig", () => {
  it("defaults to development-safe values", () => {
    expect(loadConfig({})).toEqual({
      appName: "forgebase-node",
      appEnv: "development",
      logLevel: "info",
    });
  });

  it("applies environment overrides", () => {
    const config = loadConfig({ APP_NAME: "my-app", APP_ENV: "production", LOG_LEVEL: "DEBUG" });
    expect(config).toEqual({ appName: "my-app", appEnv: "production", logLevel: "debug" });
  });

  it("fails fast on invalid values", () => {
    expect(() => loadConfig({ APP_ENV: "staging" })).toThrow(ConfigError);
    expect(() => loadConfig({ LOG_LEVEL: "verbose" })).toThrow(ConfigError);
    expect(() => loadConfig({ APP_NAME: "  " })).toThrow(ConfigError);
  });

  it("documents allowed values in the error message", () => {
    expect(() => loadConfig({ APP_ENV: "staging" })).toThrow(/development, testing, production/);
  });
});

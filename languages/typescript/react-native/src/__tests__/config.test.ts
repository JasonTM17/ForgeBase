import { loadConfig } from "../config";

describe("loadConfig", () => {
  it("exposes the required service name", () => {
    expect(loadConfig({ EXPO_PUBLIC_SERVICE_NAME: "my-app" }).serviceName).toBe(
      "my-app",
    );
  });

  it("fails fast when the service name is missing", () => {
    expect(() => loadConfig({})).toThrow(/EXPO_PUBLIC_SERVICE_NAME/);
  });

  it("fails fast on a blank service name", () => {
    expect(() => loadConfig({ EXPO_PUBLIC_SERVICE_NAME: "   " })).toThrow(
      /EXPO_PUBLIC_SERVICE_NAME/,
    );
  });

  it("falls back to the default API base URL", () => {
    expect(loadConfig({ EXPO_PUBLIC_SERVICE_NAME: "my-app" }).apiBaseUrl).toBe(
      "http://localhost:8080",
    );
  });

  it("keeps the app-level config import usable under jest setup", () => {
    expect(loadConfig(process.env).serviceName).toBe("test-service");
  });
});

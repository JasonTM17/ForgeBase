import { describe, expect, it, vi } from "vitest";

vi.mock("$env/dynamic/public", () => ({
  env: { PUBLIC_APP_NAME: "forgebase-sveltekit" },
}));

import { appName } from "../src/lib/config.js";
import { ExampleService } from "../src/lib/exampleService.js";
import { load } from "../src/routes/+page.server.js";

describe("SvelteKit starter", () => {
  it("loads typed public config", () => {
    expect(appName).toBe("forgebase-sveltekit");
  });

  it("loads page data through the SvelteKit server load function", () => {
    expect(load()).toEqual({ items: [] });
  });

  it("ExampleService creates items", () => {
    const s = new ExampleService();
    expect(s.create("first")).toEqual({ id: 1, name: "first" });
    expect(s.list()).toHaveLength(1);
  });

  it("ExampleService rejects blank names", () => {
    expect(() => new ExampleService().create("   ")).toThrow(/must not be empty/);
  });

  it("ExampleService is isolated per instance", () => {
    const a = new ExampleService();
    a.create("only-in-a");
    expect(new ExampleService().list()).toHaveLength(0);
  });
});

import { describe, expect, it } from "vitest";

import { ExampleService } from "../server/api/service.ts";

describe("Nuxt starter", () => {
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

import { describe, expect, it } from "vitest";

import { ExampleService } from "../src/example.js";

describe("ExampleService", () => {
  it("creates items with sequential ids", () => {
    const service = new ExampleService();
    expect(service.create("a")).toEqual({ id: 1, name: "a" });
    expect(service.create("b")).toEqual({ id: 2, name: "b" });
  });

  it("returns created items by id", () => {
    const service = new ExampleService();
    service.create("a");
    expect(service.get(1)).toEqual({ id: 1, name: "a" });
  });

  it("throws for unknown ids", () => {
    expect(() => new ExampleService().get(99)).toThrow("not found");
  });

  it("rejects blank names", () => {
    expect(() => new ExampleService().create("   ")).toThrow("must not be empty");
  });

  it("lists all items", () => {
    const service = new ExampleService();
    service.create("a");
    service.create("b");
    expect(service.list()).toEqual([
      { id: 1, name: "a" },
      { id: 2, name: "b" },
    ]);
  });
});

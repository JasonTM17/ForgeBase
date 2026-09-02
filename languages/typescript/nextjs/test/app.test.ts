import { describe, expect, it } from "vitest";
import "@testing-library/jest-dom/vitest";

import { ExampleService } from "../src/app/examples/service.js";

describe("Next.js starter", () => {
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
    const b = new ExampleService();
    a.create("only-in-a");
    expect(a.list()).toHaveLength(1);
    expect(b.list()).toHaveLength(0);
  });
});

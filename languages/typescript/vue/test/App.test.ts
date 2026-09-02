import { describe, expect, it } from "vitest";
import { render, fireEvent, screen } from "@testing-library/vue";
import "@testing-library/jest-dom/vitest";

import App from "../src/App.js";
import { ExampleService } from "../src/services/exampleService.js";

describe("Vue starter", () => {
  it("renders the heading", () => {
    render(App);
    expect(screen.getByRole("heading", { name: /ForgeBase Vue Starter/ })).toBeInTheDocument();
  });

  it("ExampleService creates items", () => {
    const s = new ExampleService();
    expect(s.create("first")).toEqual({ id: 1, name: "first" });
    expect(s.list()).toHaveLength(1);
  });

  it("ExampleService rejects blank names", () => {
    expect(() => new ExampleService().create("   ")).toThrow(/must not be empty/);
  });

  it("Add button is present", () => {
    render(App);
    expect(screen.getByRole("button", { name: "Add" })).toBeInTheDocument();
  });
});

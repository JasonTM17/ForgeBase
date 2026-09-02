import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";

import App from "../src/App.js";
import { ExampleService } from "../src/services/exampleService.js";

describe("React starter", () => {
  it("renders the heading", () => {
    render(<App />);
    expect(screen.getByRole("heading", { name: /ForgeBase React Starter/ })).toBeInTheDocument();
  });

  it("ExampleService creates items", () => {
    const service = new ExampleService();
    expect(service.create("first")).toEqual({ id: 1, name: "first" });
    expect(service.list()).toHaveLength(1);
  });

  it("ExampleService rejects blank names", () => {
    expect(() => new ExampleService().create("   ")).toThrow(/must not be empty/);
  });

  it("Add button is present", () => {
    render(<App />);
    expect(screen.getByRole("button", { name: "Add" })).toBeInTheDocument();
  });
});

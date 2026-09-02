import { beforeEach, describe, expect, it } from "vitest";
import request from "supertest";

import { buildApp } from "../src/app.js";
import { loadConfig } from "../src/config.js";
import { createLogger } from "../src/logger.js";
import { ExampleService, exampleService } from "../src/services/exampleService.js";

interface Envelope {
  status?: string;
  data?: unknown;
  message?: string;
  error?: { code: string; message: string; details?: unknown };
}

// Fresh in-memory store per test by replacing the module-level singleton.
beforeEach(() => {
  const fresh = new ExampleService();
  exampleService.create = fresh.create.bind(fresh);
  exampleService.get = fresh.get.bind(fresh);
  exampleService.list = fresh.list.bind(fresh);
});

const config = loadConfig({ APP_ENV: "testing", APP_PORT: "3000" });
const logger = createLogger({ ...config, logLevel: "error" });
const app = buildApp(config, logger);

describe("health endpoints", () => {
  it("GET /health returns ok", async () => {
    const res = await request(app).get("/health");
    expect(res.status).toBe(200);
    expect(res.body).toEqual({ status: "ok" });
  });

  it("GET /health/live and /health/ready return ok", async () => {
    expect((await request(app).get("/health/live")).body).toEqual({ status: "ok" });
    expect((await request(app).get("/health/ready")).body).toEqual({ status: "ok" });
  });
});

describe("example resource", () => {
  it("creates with the envelope", async () => {
    const res = await request(app).post("/api/v1/examples").send({ name: "first" });
    expect(res.status).toBe(201);
    expect(res.body).toEqual({ data: { id: 1, name: "first" }, message: "created" });
  });

  it("lists and gets created items", async () => {
    await request(app).post("/api/v1/examples").send({ name: "a" });
    await request(app).post("/api/v1/examples").send({ name: "b" });
    const list = (await request(app).get("/api/v1/examples")).body as Envelope;
    expect((list.data as Array<{ name: string }>).map((item) => item.name)).toEqual(["a", "b"]);
    const got = (await request(app).get("/api/v1/examples/2")).body as Envelope;
    expect((got.data as { name: string }).name).toBe("b");
  });

  it("rejects blank names with the validation envelope", async () => {
    const res = await request(app).post("/api/v1/examples").send({ name: "" });
    expect(res.status).toBe(422);
    expect((res.body as Envelope).error?.code).toBe("VALIDATION_ERROR");
  });
});

describe("error envelope", () => {
  it("returns the envelope for unknown routes", async () => {
    const res = await request(app).get("/api/v1/does-not-exist");
    expect(res.status).toBe(404);
    expect((res.body as Envelope).error?.code).toBe("NOT_FOUND");
  });

  it("returns the envelope for unknown resources", async () => {
    const res = await request(app).get("/api/v1/examples/999");
    expect(res.status).toBe(404);
    expect((res.body as Envelope).error?.code).toBe("RESOURCE_NOT_FOUND");
  });

  it("never leaks stack traces on client errors", async () => {
    const res = await request(app).get("/api/v1/examples/not-a-number");
    // Invalid ids are client errors mapped to a stable code, not 500s.
    expect(res.status).toBe(400);
    expect((res.body as Envelope).error?.code).toBe("INVALID_ID");
    expect(JSON.stringify(res.body)).not.toContain("at ");
  });
});

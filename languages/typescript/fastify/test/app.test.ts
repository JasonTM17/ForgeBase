import { afterAll, beforeAll, beforeEach, describe, expect, it } from "vitest";
import request from "supertest";

import { buildApp } from "../src/server.js";
import { exampleService } from "../src/services/exampleService.js";

let server: ReturnType<typeof buildApp>;

beforeAll(async () => {
  process.env.APP_ENV = "testing";
  process.env.APP_PORT = "3000";
  server = buildApp();
  await server.ready();
});

beforeEach(() => exampleService.reset());

afterAll(() => server.close());

describe("Fastify starter", () => {
  it("GET /health returns ok", async () => {
    const res = await request(server.server).get("/health");
    expect(res.status).toBe(200);
    expect(res.body).toEqual({ status: "ok" });
  });

  it("/health/live and /health/ready return ok", async () => {
    expect((await request(server.server).get("/health/live")).body).toEqual({ status: "ok" });
    expect((await request(server.server).get("/health/ready")).body).toEqual({ status: "ok" });
  });

  it("creates with the envelope", async () => {
    const res = await request(server.server).post("/api/v1/examples").send({ name: "first" });
    expect(res.status).toBe(201);
    expect(res.body).toEqual({ data: { id: 1, name: "first" }, message: "created" });
  });

  it("lists and gets", async () => {
    await request(server.server).post("/api/v1/examples").send({ name: "a" });
    await request(server.server).post("/api/v1/examples").send({ name: "b" });
    const list = await request(server.server).get("/api/v1/examples");
    expect(list.body.data.map((i: { name: string }) => i.name)).toEqual(["a", "b"]);
  });

  it("rejects blank names with validation envelope", async () => {
    const res = await request(server.server).post("/api/v1/examples").send({ name: "" });
    expect(res.status).toBe(422);
    expect(res.body.error.code).toBe("VALIDATION_ERROR");
  });

  it("returns error envelope for unknown route", async () => {
    const res = await request(server.server).get("/api/v1/does-not-exist");
    expect(res.status).toBe(404);
    expect(res.body.error.code).toBe("NOT_FOUND");
  });

  it("returns error envelope for unknown resource", async () => {
    const res = await request(server.server).get("/api/v1/examples/999");
    expect(res.status).toBe(404);
    expect(res.body.error.code).toBe("RESOURCE_NOT_FOUND");
  });
});

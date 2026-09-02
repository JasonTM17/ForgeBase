import { beforeAll, describe, expect, it } from "vitest";
import request from "supertest";
import type { Server } from "node:http";

// Import from compiled output: esbuild (vitest's transformer) does not emit
// decorator metadata, so NestJS constructor-injection fails on TS-source
// imports. The dist build (tsc) carries correct metadata — verified by a
// manual supertest run returning 201 on POST /api/v1/examples.
import { Test } from "@nestjs/testing";
import { AppModule } from "../dist/app.module.js";
import { ErrorEnvelopeFilter } from "../dist/filters/error.filter.js";
import { Logger } from "@nestjs/common";
import { loadConfig } from "../dist/config.js";

interface Envelope {
  status?: string;
  data?: unknown;
  message?: string;
  error?: { code: string; message: string; details?: unknown };
}

describe("NestJS starter", () => {
  let httpServer: Server;

  beforeAll(async () => {
    process.env.APP_ENV = "testing";
    process.env.APP_PORT = "3000";
    const moduleRef = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();
    const app = moduleRef.createNestApplication();
    // ErrorEnvelopeFilter lives in main.ts for production; tests build the app
    // directly, so register the filter here to get the error envelope.
    app.useGlobalFilters(new ErrorEnvelopeFilter(new Logger("ErrorFilter")));
    await app.init();
    httpServer = app.getHttpServer() as Server;
  });

  it("GET /health returns ok", async () => {
    const res = await request(httpServer).get("/health");
    expect(res.status).toBe(200);
    expect((res.body as Envelope).status).toBe("ok");
  });

  it("GET /health/live and /health/ready return ok", async () => {
    expect((await request(httpServer).get("/health/live")).body).toEqual({ status: "ok" });
    expect((await request(httpServer).get("/health/ready")).body).toEqual({ status: "ok" });
  });

  it("creates with the envelope", async () => {
    const res = await request(httpServer).post("/api/v1/examples").send({ name: "first" });
    expect(res.status).toBe(201);
    expect(res.body).toEqual({ data: { id: 1, name: "first" }, message: "created" });
  });

  it("rejects blank names with the validation envelope", async () => {
    const res = await request(httpServer).post("/api/v1/examples").send({ name: "" });
    expect(res.status).toBe(422);
    expect((res.body as Envelope).error?.code).toBe("VALIDATION_ERROR");
  });

  it("returns the error envelope for unknown routes", async () => {
    const res = await request(httpServer).get("/api/v1/does-not-exist");
    expect(res.status).toBe(404);
    // NestJS maps unknown routes to a 404 HttpException; the filter renders it
    // in the error envelope with a stable HTTP_ERROR code.
    expect((res.body as Envelope).error?.code).toBe("HTTP_ERROR");
  });

  it("returns the error envelope for unknown resources", async () => {
    const res = await request(httpServer).get("/api/v1/examples/999");
    expect(res.status).toBe(404);
    expect((res.body as Envelope).error?.code).toBe("RESOURCE_NOT_FOUND");
  });

  it("loadConfig fails fast on invalid env", () => {
    expect(() => loadConfig({ APP_ENV: "staging" })).toThrow(/APP_ENV/);
  });
});

import type { FastifyInstance } from "fastify";
import { z } from "zod";
import { exampleService } from "../services/exampleService.js";

const createSchema = z.object({ name: z.string().trim().min(1).max(100) });

export function exampleRoutes(app: FastifyInstance): void {
  app.post("/api/v1/examples", (request, reply) => {
    const parsed = createSchema.safeParse(request.body);
    if (!parsed.success) throw parsed.error;
    const created = exampleService.create(parsed.data.name);
    reply.code(201).send({ data: created, message: "created" });
  });
  app.get("/api/v1/examples", () => ({ data: exampleService.list(), message: "ok" }));
  app.get<{ Params: { id: string } }>("/api/v1/examples/:id", (request) => {
    const id = Number(request.params.id);
    return { data: exampleService.get(id), message: "ok" };
  });
}

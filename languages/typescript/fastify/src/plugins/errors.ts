import type { FastifyInstance, FastifyReply } from "fastify";
import { ZodError } from "zod";
import { DomainError } from "../errors.js";

export function registerErrorHook(app: FastifyInstance): void {
  app.setErrorHandler((error, _request, reply: FastifyReply) => {
    if (error instanceof ZodError) {
      reply
        .code(422)
        .send({
          error: {
            code: "VALIDATION_ERROR",
            message: "Request validation failed",
            details: error.issues,
          },
        });
      return;
    }
    if (error instanceof DomainError) {
      reply.code(error.status).send({ error: { code: error.code, message: error.message } });
      return;
    }
    const httpError = error as { statusCode?: number; message?: string };
    if (
      typeof httpError?.statusCode === "number" &&
      httpError.statusCode >= 400 &&
      httpError.statusCode < 500
    ) {
      reply
        .code(httpError.statusCode)
        .send({ error: { code: "HTTP_ERROR", message: httpError.message ?? "Client error" } });
      return;
    }
    app.log.error({ err: error }, "unhandled error");
    reply
      .code(500)
      .send({ error: { code: "INTERNAL_ERROR", message: "An unexpected error occurred" } });
  });

  app.setNotFoundHandler((_request, reply: FastifyReply) => {
    reply.code(404).send({ error: { code: "NOT_FOUND", message: "Route not found" } });
  });
}

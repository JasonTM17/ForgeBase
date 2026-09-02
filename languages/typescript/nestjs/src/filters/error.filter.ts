import { ArgumentsHost, Catch, ExceptionFilter, HttpException, Logger } from "@nestjs/common";
import { Request, Response } from "express";
import { ZodError } from "zod";

import { DomainError } from "../errors.js";

/**
 * Central exception filter — the single place errors become HTTP responses.
 * Every response follows the error envelope; internals never leak.
 */
@Catch()
export class ErrorEnvelopeFilter implements ExceptionFilter {
  private readonly logger: Logger;

  constructor(logger?: Logger) {
    this.logger = logger ?? new Logger("ErrorFilter");
  }

  catch(exception: unknown, host: ArgumentsHost): void {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();
    const err = exception as Error & { getStatus?: () => number; status?: number; code?: string };

    if (exception instanceof ZodError) {
      response.status(422).json({
        error: {
          code: "VALIDATION_ERROR",
          message: "Request validation failed",
          details: exception.issues,
        },
      });
      return;
    }

    if (exception instanceof DomainError) {
      response.status(err.status as number).json({
        error: { code: err.code as string, message: err.message },
      });
      return;
    }

    // NestJS HttpException (4xx) — safe to surface its message.
    if (exception instanceof HttpException) {
      const status = (err as { getStatus: () => number }).getStatus();
      response.status(status).json({
        error: { code: "HTTP_ERROR", message: (err as Error).message },
      });
      return;
    }

    this.logger.error(
      exception instanceof Error ? (exception.stack ?? exception.message) : String(exception),
      request.url,
    );
    response.status(500).json({
      error: { code: "INTERNAL_ERROR", message: "An unexpected error occurred" },
    });
  }
}

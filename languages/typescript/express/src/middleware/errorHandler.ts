/**
 * Central error handler — the single place errors become HTTP responses.
 *
 * Every error response follows the envelope:
 *   {"error": {"code": "...", "message": "..."}}
 * Production responses never leak stack traces or internals.
 */

import { type NextFunction, type Request, type Response } from "express";
import { ZodError } from "zod";

import { DomainError } from "../errors.js";
import type { Logger } from "../logger.js";

interface HttpError extends Error {
  status?: number;
  code?: string;
}

export function errorHandler(logger: Logger) {
  return (err: unknown, _req: Request, res: Response, next: NextFunction): void => {
    if (res.headersSent) {
      next(err);
      return;
    }

    if (err instanceof ZodError) {
      res.status(422).json({
        error: {
          code: "VALIDATION_ERROR",
          message: "Request validation failed",
          details: err.issues,
        },
      });
      return;
    }

    if (err instanceof DomainError) {
      res.status(err.status).json({ error: { code: err.code, message: err.message } });
      return;
    }

    const httpError = err as HttpError;
    if (
      typeof httpError?.status === "number" &&
      httpError.status >= 400 &&
      httpError.status < 500
    ) {
      res.status(httpError.status).json({
        error: { code: httpError.code ?? "HTTP_ERROR", message: httpError.message },
      });
      return;
    }

    // Unexpected errors: log server-side, return nothing actionable.
    logger.error({ err }, "unhandled error");
    res.status(500).json({
      error: { code: "INTERNAL_ERROR", message: "An unexpected error occurred" },
    });
  };
}

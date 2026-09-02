/**
 * Domain errors with stable machine-readable codes.
 *
 * Services throw these; the central error handler maps them to the error
 * envelope. Unexpected errors collapse to a generic 500 — details are logged
 * server-side, never returned.
 */

export class DomainError extends Error {
  readonly code: string;
  readonly status: number;

  constructor(code: string, status: number, message: string) {
    super(message);
    this.code = code;
    this.status = status;
  }
}

export class NotFoundError extends DomainError {
  constructor(message: string) {
    super("RESOURCE_NOT_FOUND", 404, message);
  }
}

export class AlreadyExistsError extends DomainError {
  constructor(message: string) {
    super("RESOURCE_ALREADY_EXISTS", 409, message);
  }
}

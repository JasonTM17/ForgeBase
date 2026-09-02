/**
 * Domain errors with stable codes. Services throw these; the global exception
 * filter maps them to the error envelope.
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

package com.forgebase.springboot;

/**
 * Expected, user-facing domain error.
 * <p>
 * Thrown by services; mapped to an RFC 9457 ProblemDetail response by the
 * global handler.
 */
public class DomainError extends RuntimeException {
    private final String code;
    private final int status;

    protected DomainError(String code, int status, String message) {
        super(message);
        this.code = code;
        this.status = status;
    }

    public String getCode() {
        return code;
    }

    public int getStatus() {
        return status;
    }

    public static DomainError notFound(String message) {
        return new DomainError("RESOURCE_NOT_FOUND", 404, message);
    }
}

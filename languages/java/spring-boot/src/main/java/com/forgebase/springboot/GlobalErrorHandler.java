package com.forgebase.springboot;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.ProblemDetail;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;
import org.springframework.web.servlet.mvc.method.annotation.ResponseEntityExceptionHandler;

import java.net.URI;

/**
 * Central error handler — the single place exceptions become HTTP responses.
 * <p>
 * Domain errors map to RFC 9457 ProblemDetail (a consistent error contract);
 * unexpected exceptions collapse to a generic 500 with no internal details
 * leaked. Framework-raised exceptions (validation, malformed JSON, missing
 * routes) are handled by {@link ResponseEntityExceptionHandler}, which
 * renders them as ProblemDetail on this Spring Boot version.
 */
@RestControllerAdvice
public class GlobalErrorHandler extends ResponseEntityExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalErrorHandler.class);

    @ExceptionHandler(DomainError.class)
    public ProblemDetail handleDomain(DomainError error) {
        ProblemDetail problem = ProblemDetail.forStatus(HttpStatus.valueOf(error.getStatus()));
        problem.setTitle(error.getCode());
        problem.setDetail(error.getMessage());
        problem.setType(URI.create("https://forgebase.dev/errors/" + error.getCode()));
        return problem;
    }

    @ExceptionHandler(IllegalArgumentException.class)
    public ProblemDetail handleValidation(IllegalArgumentException error) {
        ProblemDetail problem = ProblemDetail.forStatus(HttpStatus.BAD_REQUEST);
        problem.setTitle("INVALID_ARGUMENT");
        problem.setDetail(error.getMessage());
        problem.setType(URI.create("https://forgebase.dev/errors/INVALID_ARGUMENT"));
        return problem;
    }

    @ExceptionHandler(Exception.class)
    public ProblemDetail handleUnexpected(Exception error) {
        // Log the full failure server-side; clients get nothing actionable.
        log.error("unhandled exception", error);
        ProblemDetail problem = ProblemDetail.forStatus(HttpStatus.INTERNAL_SERVER_ERROR);
        problem.setTitle("INTERNAL_ERROR");
        problem.setDetail("An unexpected error occurred");
        problem.setType(URI.create("https://forgebase.dev/errors/INTERNAL_ERROR"));
        return problem;
    }
}

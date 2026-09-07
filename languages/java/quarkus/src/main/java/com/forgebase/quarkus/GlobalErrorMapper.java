package com.forgebase.quarkus;

import com.fasterxml.jackson.core.JsonProcessingException;

import jakarta.ws.rs.BadRequestException;
import jakarta.ws.rs.WebApplicationException;
import jakarta.ws.rs.core.Response;
import jakarta.ws.rs.ext.ExceptionMapper;
import jakarta.ws.rs.ext.Provider;

import java.util.Map;

/**
 * Central error mapper — the single place exceptions become HTTP responses.
 * Every error follows the envelope: {"error": {"code", "message"}}. The
 * nested mappers are registered individually; the container class itself is
 * not a mapper.
 */
public class GlobalErrorMapper {

    @Provider
    public static class NotFoundMapper implements ExceptionMapper<NotFoundException> {
        @Override
        public Response toResponse(NotFoundException exception) {
            return Response.status(404)
                    .entity(Map.of("error", Map.of("code", "RESOURCE_NOT_FOUND", "message", exception.getMessage())))
                    .build();
        }
    }

    @Provider
    public static class IllegalArgumentMapper implements ExceptionMapper<IllegalArgumentException> {
        @Override
        public Response toResponse(IllegalArgumentException exception) {
            return Response.status(400)
                    .entity(Map.of("error", Map.of("code", "INVALID_ARGUMENT", "message", exception.getMessage())))
                    .build();
        }
    }

    @Provider
    public static class MalformedJsonMapper implements ExceptionMapper<JsonProcessingException> {
        @Override
        public Response toResponse(JsonProcessingException exception) {
            return Response.status(400)
                    .entity(Map.of("error", Map.of("code", "INVALID_ARGUMENT", "message", "malformed JSON body")))
                    .build();
        }
    }

    @Provider
    public static class BadRequestMapper implements ExceptionMapper<BadRequestException> {
        @Override
        public Response toResponse(BadRequestException exception) {
            return Response.status(400)
                    .entity(Map.of("error", Map.of("code", "INVALID_ARGUMENT", "message", "malformed JSON body")))
                    .build();
        }
    }

    @Provider
    public static class GenericMapper implements ExceptionMapper<Exception> {
        @Override
        public Response toResponse(Exception exception) {
            if (exception instanceof BadRequestException || hasCause(exception, JsonProcessingException.class)) {
                return Response.status(400)
                        .entity(Map.of("error", Map.of("code", "INVALID_ARGUMENT", "message", "malformed JSON body")))
                        .build();
            }

            if (exception instanceof WebApplicationException webApplicationException) {
                int status = webApplicationException.getResponse().getStatus();
                if (status >= 400 && status < 500) {
                    return Response.status(status)
                            .entity(Map.of("error", Map.of("code", "REQUEST_ERROR", "message", "Request could not be processed")))
                            .build();
                }
            }

            return Response.status(500)
                    .entity(Map.of("error", Map.of("code", "INTERNAL_ERROR", "message", "An unexpected error occurred")))
                    .build();
        }

        private boolean hasCause(Throwable exception, Class<? extends Throwable> causeType) {
            Throwable current = exception;
            while (current != null) {
                if (causeType.isInstance(current)) {
                    return true;
                }
                current = current.getCause();
            }
            return false;
        }
    }
}

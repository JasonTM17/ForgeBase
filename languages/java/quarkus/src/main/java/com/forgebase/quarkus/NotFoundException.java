package com.forgebase.quarkus;

/** Expected, user-facing domain error. */
public class NotFoundException extends RuntimeException {
    public NotFoundException(String message) {
        super(message);
    }
}

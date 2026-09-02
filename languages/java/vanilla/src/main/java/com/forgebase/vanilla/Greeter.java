package com.forgebase.vanilla;

/**
 * Example service demonstrating the testable service-layer pattern.
 * Deliberately generic.
 */
public class Greeter {
    public String greet(String name) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("name must not be empty");
        }
        return "Hello, " + name.trim() + "!";
    }
}

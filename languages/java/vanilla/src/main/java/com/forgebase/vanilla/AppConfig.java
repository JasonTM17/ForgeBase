package com.forgebase.vanilla;

/**
 * Fail-fast environment configuration.
 *
 * Misconfiguration must stop the process at boot with a message that names
 * the offending variable.
 */
public final class AppConfig {
    private static final String DEFAULT_NAME = "forgebase-java";
    private static final String DEFAULT_ENV = "development";

    private AppConfig() {
    }

    public static String appName() {
        return trimOrDefault(System.getenv("APP_NAME"), DEFAULT_NAME);
    }

    public static String appEnv() {
        String value = trimOrDefault(System.getenv("APP_ENV"), DEFAULT_ENV);
        return switch (value) {
            case "development", "testing", "production" -> value;
            default -> throw new IllegalArgumentException(
                    "APP_ENV must be one of development, testing, production, got " + value);
        };
    }

    private static String trimOrDefault(String value, String defaultValue) {
        if (value == null || value.isBlank()) {
            return defaultValue;
        }
        return value.trim();
    }
}

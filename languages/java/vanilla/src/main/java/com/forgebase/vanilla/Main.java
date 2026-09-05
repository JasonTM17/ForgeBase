package com.forgebase.vanilla;

/**
 * CLI entry point: {@code java -cp target/classes com.forgebase.vanilla.Main <name>}
 * or via {@code mvn exec:java -Dexec.args="World"}.
 */
public final class Main {
    public static void main(String[] args) {
        try {
            // Validate process configuration before handling user input or
            // invoking the service layer.
            AppConfig.appEnv();
        } catch (IllegalArgumentException exc) {
            System.err.println("configuration error: " + exc.getMessage());
            System.exit(2);
            return;
        }

        String name = args.length > 0 ? args[0] : null;
        if (name == null || name.isBlank()) {
            System.err.println("usage: Main <name>");
            System.exit(1);
        }
        try {
            System.out.println(new Greeter().greet(name));
        } catch (IllegalArgumentException exc) {
            // Expected errors: surface the message, not a stack trace.
            System.err.println("error: " + exc.getMessage());
            System.exit(1);
        }
    }
}

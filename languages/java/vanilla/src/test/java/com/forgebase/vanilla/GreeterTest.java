package com.forgebase.vanilla;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class GreeterTest {
    @Test
    void greetsTheName() {
        assertEquals("Hello, World!", new Greeter().greet("World"));
    }

    @Test
    void trimsWhitespace() {
        assertEquals("Hello, World!", new Greeter().greet("  World  "));
    }

    @Test
    void rejectsBlankName() {
        IllegalArgumentException ex = assertThrows(IllegalArgumentException.class,
                () -> new Greeter().greet("   "));
        assertTrue(ex.getMessage().contains("must not be empty"));
    }
}

class AppConfigTest {
    @Test
    void defaultsAreDevelopmentSafe() {
        assertEquals("development", AppConfig.appEnv());
        assertEquals("forgebase-java", AppConfig.appName());
    }
}

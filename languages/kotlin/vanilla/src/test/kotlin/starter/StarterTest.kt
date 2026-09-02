package starter

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith
import kotlin.test.assertNull

class EnvConfigTest {
    @Test
    fun `throws when required variable is missing`() {
        val error = assertFailsWith<EnvConfigException> {
            EnvConfig.fromEnvironment(emptyMap())
        }
        assertEquals(
            "required environment variable SERVICE_NAME is missing or empty",
            error.message,
        )
    }

    @Test
    fun `throws when required variable is blank`() {
        assertFailsWith<EnvConfigException> {
            EnvConfig.fromEnvironment(mapOf("SERVICE_NAME" to "  "))
        }
    }

    @Test
    fun `defaults log level to information`() {
        val config = EnvConfig.fromEnvironment(mapOf("SERVICE_NAME" to "demo"))
        assertEquals(LogSeverity.INFORMATION, config.logLevel)
    }

    @Test
    fun `throws on unknown log level`() {
        assertFailsWith<EnvConfigException> {
            EnvConfig.fromEnvironment(
                mapOf("SERVICE_NAME" to "demo", "APP_LOG_LEVEL" to "loud"),
            )
        }
    }

    @Test
    fun `parses log level case insensitively`() {
        val config = EnvConfig.fromEnvironment(
            mapOf("SERVICE_NAME" to "demo", "APP_LOG_LEVEL" to "Warning"),
        )
        assertEquals(LogSeverity.WARNING, config.logLevel)
    }
}

class LogSeverityTest {
    @Test
    fun `orders by severity not alphabetically`() {
        assert(LogSeverity.ERROR < LogSeverity.INFORMATION)
        assert(LogSeverity.CRITICAL < LogSeverity.DEBUG)
    }

    @Test
    fun `parse returns null for unknown names`() {
        assertNull(LogSeverity.parse("loud"))
        assertNull(LogSeverity.parse(""))
    }
}

class GreeterTest {
    @Test
    fun `greets by name`() {
        assertEquals("Hello, ForgeBase!", Greeter().greet("ForgeBase"))
    }

    @Test
    fun `rejects empty names`() {
        assertFailsWith<IllegalArgumentException> {
            Greeter().greet("   ")
        }
    }
}

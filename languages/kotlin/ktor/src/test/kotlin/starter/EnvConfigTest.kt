package starter

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertFailsWith

class EnvConfigTest {
    @Test
    fun `valid environment loads with defaults`() {
        val config = EnvConfig.fromEnvironment(mapOf("SERVICE_NAME" to "demo"))
        assertEquals("demo", config.serviceName)
        assertEquals(LogSeverity.INFORMATION, config.logLevel)
        assertEquals(8080, config.port)
    }

    @Test
    fun `missing service name aborts startup`() {
        assertFailsWith<EnvConfigException> {
            EnvConfig.fromEnvironment(emptyMap())
        }
    }

    @Test
    fun `unknown log level aborts startup`() {
        assertFailsWith<EnvConfigException> {
            EnvConfig.fromEnvironment(mapOf("SERVICE_NAME" to "demo", "APP_LOG_LEVEL" to "loud"))
        }
    }

    @Test
    fun `non numeric port aborts startup`() {
        assertFailsWith<EnvConfigException> {
            EnvConfig.fromEnvironment(mapOf("SERVICE_NAME" to "demo", "PORT" to "http"))
        }
    }
}

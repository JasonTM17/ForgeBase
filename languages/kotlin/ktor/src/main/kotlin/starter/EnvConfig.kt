package starter

/**
 * Fail-fast configuration: missing required variables or values that fail
 * validation abort startup before any real work happens.
 */
data class EnvConfig(
    val serviceName: String,
    val logLevel: LogSeverity,
    val port: Int,
) {
    companion object {
        fun fromEnvironment(environment: Map<String, String> = System.getenv()): EnvConfig {
            val serviceName = required(environment, "SERVICE_NAME")
            val levelName = optional(environment, "APP_LOG_LEVEL", "information")
            val logLevel = LogSeverity.parse(levelName)
                ?: throw EnvConfigException(
                    "APP_LOG_LEVEL '$levelName' is invalid. Valid values: " +
                        LogSeverity.entries.joinToString(", ") { it.name.lowercase() } + ".",
                )
            val portRaw = optional(environment, "PORT", "8080")
            val port = portRaw.toIntOrNull() ?: throw EnvConfigException(
                "PORT '$portRaw' is invalid. Expected an integer in 1..65535.",
            )
            return EnvConfig(serviceName, logLevel, port)
        }

        private fun required(environment: Map<String, String>, name: String): String {
            val value = environment[name]
            if (value.isNullOrBlank()) {
                throw EnvConfigException(
                    "required environment variable $name is missing or empty",
                )
            }
            return value
        }

        private fun optional(environment: Map<String, String>, name: String, fallback: String): String {
            val value = environment[name]
            return if (value.isNullOrBlank()) fallback else value
        }
    }
}

class EnvConfigException(message: String) : RuntimeException(message)

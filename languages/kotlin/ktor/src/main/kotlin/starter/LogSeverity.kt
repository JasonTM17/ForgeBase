package starter

/**
 * Severity levels for the built-in console logger, ordered from most to
 * least severe. The declaration order is the severity order.
 */
enum class LogSeverity {
    CRITICAL, ERROR, WARNING, INFORMATION, DEBUG, TRACE;

    val tag: String
        get() = name.take(3)

    val isError: Boolean
        get() = this <= ERROR

    companion object {
        fun parse(value: String): LogSeverity? =
            entries.firstOrNull { it.name.equals(value.trim(), ignoreCase = true) }
    }
}

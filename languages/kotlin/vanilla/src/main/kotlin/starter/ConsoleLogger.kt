package starter

import java.time.ZonedDateTime
import java.time.format.DateTimeFormatter

/**
 * Minimal leveled logger: ISO-8601 UTC timestamp, severity tag, and service
 * context on every line. Errors go to stderr so redirection keeps
 * diagnostics out of data pipelines. Replace with a structured logging
 * library when the copied-out project needs richer sinks.
 */
class ConsoleLogger(
    private val threshold: LogSeverity,
    private val service: String,
) {
    fun info(message: String) = write(LogSeverity.INFORMATION, message)

    fun warning(message: String) = write(LogSeverity.WARNING, message)

    fun error(message: String) = write(LogSeverity.ERROR, message)

    private fun write(severity: LogSeverity, message: String) {
        if (severity > threshold) return

        val timestamp = ZonedDateTime.now(java.time.ZoneOffset.UTC)
            .format(DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss'Z'"))
        val line = "$timestamp [${severity.tag}] service=$service $message"
        if (severity.isError) {
            System.err.println(line)
        } else {
            println(line)
        }
    }
}

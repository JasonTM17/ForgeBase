package starter

import ch.qos.logback.classic.Level
import ch.qos.logback.classic.Logger
import org.slf4j.LoggerFactory

/** Map the severity enum onto logback's level names (no INFORMATION/WARNING). */
private fun LogSeverity.toLogbackLevel(): Level = when (this) {
    LogSeverity.CRITICAL, LogSeverity.ERROR -> Level.ERROR
    LogSeverity.WARNING -> Level.WARN
    LogSeverity.INFORMATION -> Level.INFO
    LogSeverity.DEBUG -> Level.DEBUG
    LogSeverity.TRACE -> Level.TRACE
}

/**
 * Applies the validated APP_LOG_LEVEL to the root logger and announces the
 * service identity, so both configured values are observable in every run.
 */
fun configureLogging(config: EnvConfig) {
    val root = LoggerFactory.getLogger(Logger.ROOT_LOGGER_NAME) as Logger
    root.level = config.logLevel.toLogbackLevel()
    root.info("starting service {}", config.serviceName)
}

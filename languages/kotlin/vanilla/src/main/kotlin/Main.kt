package starter

import kotlin.system.exitProcess

// Fail-fast demo: a missing or invalid configuration variable exits with a
// clean message and a non-zero code instead of a stack trace.
fun main() {
    val config = try {
        EnvConfig.fromEnvironment()
    } catch (error: EnvConfigException) {
        System.err.println("configuration error: ${error.message}")
        exitProcess(2)
    }

    val logger = ConsoleLogger(config.logLevel, config.serviceName)
    logger.info("service starting")
    println(Greeter().greet("ForgeBase"))
    logger.info("service finished")
}

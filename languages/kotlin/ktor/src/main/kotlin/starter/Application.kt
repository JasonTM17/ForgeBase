package starter

import io.ktor.server.application.Application
import io.ktor.server.application.install
import io.ktor.server.engine.embeddedServer
import io.ktor.server.netty.Netty
import io.ktor.server.plugins.contentnegotiation.ContentNegotiation
import io.ktor.server.routing.routing
import io.ktor.serialization.kotlinx.json.json
import kotlinx.serialization.json.Json

/** Wires the production plugins/routes; reused by the test host. */
fun Application.module() {
    install(ContentNegotiation) { json(Json { prettyPrint = true }) }
    installErrorPages()
    routing { apiRoutes() }
}

fun main() {
    val config = try {
        EnvConfig.fromEnvironment()
    } catch (error: EnvConfigException) {
        System.err.println("configuration error: ${error.message}")
        kotlin.system.exitProcess(2)
    }
    configureLogging(config)

    embeddedServer(Netty, port = config.port, host = "0.0.0.0", module = {
        module()
    }).start(wait = true)
}

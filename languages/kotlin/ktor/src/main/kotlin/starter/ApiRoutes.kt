package starter

import io.ktor.http.HttpStatusCode
import io.ktor.server.application.call
import io.ktor.server.response.respond
import io.ktor.server.routing.Routing
import io.ktor.server.routing.delete
import io.ktor.server.routing.get
import io.ktor.server.routing.post
import kotlinx.serialization.Serializable
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.atomic.AtomicLong

@Serializable
data class Widget(val id: Long, val name: String)

@Serializable
data class CreateWidget(val name: String)

private val store = ConcurrentHashMap<Long, Widget>()
private val nextId = AtomicLong(0)

fun Routing.apiRoutes() {
    get("/health") { call.respond(mapOf("status" to "ok")) }
    get("/health/live") { call.respond(mapOf("status" to "ok")) }
    get("/health/ready") { call.respond(mapOf("status" to "ok")) }

    route("/api/widgets") {
        post {
            val body = call.receive<CreateWidget>()
            if (body.name.isBlank()) {
                throw EnvConfigException("name is required")
            }
            val id = nextId.incrementAndGet()
            val widget = Widget(id, body.name)
            store[id] = widget
            call.respond(HttpStatusCode.Created, mapOf("data" to widget, "message" to "ok"))
        }
        get {
            call.respond(mapOf("data" to store.values.sortedBy { it.id }, "message" to "ok"))
        }
        get("/{id}") {
            val id = call.parameters["id"]?.toLongOrNull() ?: throw EnvConfigException("invalid id")
            val widget = store[id] ?: throw NoSuchElementException("widget $id not found")
            call.respond(mapOf("data" to widget, "message" to "ok"))
        }
        delete("/{id}") {
            val id = call.parameters["id"]?.toLongOrNull() ?: throw EnvConfigException("invalid id")
            if (store.remove(id) == null) throw NoSuchElementException("widget $id not found")
            call.respond(HttpStatusCode.NoContent)
        }
    }
}

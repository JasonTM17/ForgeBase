package starter

import io.ktor.http.HttpStatusCode
import io.ktor.server.application.ApplicationCall
import io.ktor.server.application.install
import io.ktor.server.plugins.requestvalidation.RequestValidationException
import io.ktor.server.plugins.statuspages.StatusPages
import io.ktor.server.response.respond
import kotlinx.serialization.Serializable

/**
 * Light JSON envelope contract: {"data", "message"} on success,
 * {"error": {"code", "message"}} on failure.
 */
@Serializable
data class ErrorEnvelope(val error: ErrorBody) {
    @Serializable
    data class ErrorBody(val code: String, val message: String)
}

/** Maps one exception to an envelope response. */
private suspend fun ApplicationCall.respondError(
    status: HttpStatusCode,
    code: String,
    message: String,
) {
    respond(status, ErrorEnvelope(ErrorEnvelope.ErrorBody(code, message)))
}

/**
 * Wires the StatusPages plugin. Centralizes error handling in one place so
 * production responses never leak stack traces or internal details.
 */
fun io.ktor.server.application.Application.installErrorPages() {
    install(StatusPages) {
        exception<InvalidRequestException> { call, cause ->
            call.respondError(HttpStatusCode.BadRequest, "RESOURCE_INVALID", cause.message ?: "")
        }
        exception<NoSuchElementException> { call, cause ->
            call.respondError(HttpStatusCode.NotFound, "RESOURCE_NOT_FOUND", cause.message ?: "")
        }
        exception<RequestValidationException> { call, cause ->
            call.respondError(HttpStatusCode.BadRequest, "RESOURCE_INVALID", cause.reasons.joinToString())
        }
        exception<Throwable> { call, cause ->
            // Never surface internals: every production response carries the
            // generic envelope, never the exception detail.
            call.respondError(
                HttpStatusCode.InternalServerError,
                "INTERNAL_ERROR",
                "internal server error",
            )
        }
    }
}

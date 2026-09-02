package starter

import io.ktor.http.HttpStatusCode
import io.ktor.server.application.ApplicationCall
import io.ktor.server.plugins.requestvalidation.RequestValidationException
import io.ktor.server.plugins.statuspages.StatusPages
import io.ktor.server.response.respond

/**
 * Light JSON envelope contract: {"data", "message"} on success,
 * {"error": {"code", "message"}} on failure.
 */
data class ErrorEnvelope(val error: ErrorBody) {
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
        exception<EnvConfigException> { call, cause ->
            call.respondError(HttpStatusCode.BadRequest, "RESOURCE_INVALID", cause.message ?: "")
        }
        exception<NoSuchElementException> { call, cause ->
            call.respondError(HttpStatusCode.NotFound, "RESOURCE_NOT_FOUND", cause.message ?: "")
        }
        exception<RequestValidationException> { call, cause ->
            call.respondError(HttpStatusCode.BadRequest, "RESOURCE_INVALID", cause.reasons.joinToString())
        }
        exception<Throwable> { call, cause ->
            // Only surface details outside production.
            call.application.environment.config.developmentMode
            call.respondError(
                HttpStatusCode.InternalServerError,
                "INTERNAL_ERROR",
                "internal server error",
            )
        }
    }
}

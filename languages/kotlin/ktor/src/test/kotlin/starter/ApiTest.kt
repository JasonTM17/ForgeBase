package starter

import io.ktor.client.request.get
import io.ktor.client.request.post
import io.ktor.client.request.setBody
import io.ktor.client.statement.bodyAsText
import io.ktor.http.ContentType
import io.ktor.http.contentType
import io.ktor.server.testing.testApplication
import kotlinx.serialization.json.Json
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.jsonObject
import kotlinx.serialization.json.jsonPrimitive
import kotlin.test.Test
import kotlin.test.assertEquals

private val json = Json { ignoreUnknownKeys = true }

private fun parse(text: String): JsonObject = json.parseToJsonElement(text).jsonObject

class ApiTest {
    @Test
    fun `health trio returns ok`() = testApplication {
        application { module() }
        val client = createClient {}
        for (path in listOf("/health", "/health/live", "/health/ready")) {
            val response = client.get(path)
            assertEquals(io.ktor.http.HttpStatusCode.OK, response.status)
            assertEquals("ok", parse(response.bodyAsText())["status"]?.jsonPrimitive?.content)
        }
    }

    @Test
    fun `widget flow validates creates and rejects bad input`() = testApplication {
        application { module() }
        val client = createClient {}

        val created = client.post("/api/widgets") {
            contentType(ContentType.Application.Json)
            setBody("""{"name":"anvil"}""")
        }
        assertEquals(io.ktor.http.HttpStatusCode.Created, created.status)
        val createdBody = parse(created.bodyAsText())
        assertEquals("anvil", createdBody["data"]?.jsonObject?.get("name")?.jsonPrimitive?.content)
        val id = createdBody["data"]?.jsonObject?.get("id")?.jsonPrimitive?.content

        val fetched = client.get("/api/widgets/$id")
        assertEquals(io.ktor.http.HttpStatusCode.OK, fetched.status)
        assertEquals("anvil", parse(fetched.bodyAsText())["data"]?.jsonObject?.get("name")?.jsonPrimitive?.content)

        val invalid = client.post("/api/widgets") {
            contentType(ContentType.Application.Json)
            setBody("""{"name":"  "}""")
        }
        assertEquals(io.ktor.http.HttpStatusCode.BadRequest, invalid.status)
        assertEquals("RESOURCE_INVALID", parse(invalid.bodyAsText())["error"]?.jsonObject?.get("code")?.jsonPrimitive?.content)
    }

    @Test
    fun `missing widget returns not found envelope`() = testApplication {
        application { module() }
        val client = createClient {}

        val response = client.get("/api/widgets/999")
        assertEquals(io.ktor.http.HttpStatusCode.NotFound, response.status)
        assertEquals("RESOURCE_NOT_FOUND", parse(response.bodyAsText())["error"]?.jsonObject?.get("code")?.jsonPrimitive?.content)
    }
}

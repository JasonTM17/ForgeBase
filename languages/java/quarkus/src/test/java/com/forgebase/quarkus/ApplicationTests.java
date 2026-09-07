package com.forgebase.quarkus;

import io.quarkus.test.junit.QuarkusTest;
import io.restassured.http.ContentType;
import jakarta.inject.Inject;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;
import static org.junit.jupiter.api.Assertions.assertEquals;

@QuarkusTest
class ApplicationTests {

    @Inject
    AppConfig config;

    @Test
    void configurationIsBoundFromEnvironment() {
        // Proves the documented environment variables feed real code: the
        // mapping rejects unknown APP_ENV values at startup and the defaults
        // bind through when the variables are unset.
        assertEquals("forgebase-quarkus", config.name());
        assertEquals(AppConfig.AppEnv.DEVELOPMENT, config.env());
    }

    @Test
    void healthReturnsOk() {
        // SmallRye health root reports the aggregated status of all checks.
        given().when().get("/q/health").then().statusCode(200);
    }

    @Test
    void livenessReturnsOk() {
        given().when().get("/q/health/live").then().statusCode(200);
    }

    @Test
    void readinessReturnsOk() {
        given().when().get("/q/health/ready").then().statusCode(200);
    }

    @Test
    void createReturnsEnvelope() {
        given().contentType(ContentType.JSON).body("{\"name\":\"first\"}")
                .when().post("/api/v1/examples")
                .then().statusCode(201).body("data.id", equalTo(1)).body("data.name", equalTo("first"));
    }

    @Test
    void blankNameIsRejected() {
        given().contentType(ContentType.JSON).body("{\"name\":\"\"}")
                .when().post("/api/v1/examples")
                .then().statusCode(400).body("error.code", equalTo("INVALID_ARGUMENT"));
    }

    @Test
    void malformedJsonIsRejectedAsBadRequest() {
        given().contentType(ContentType.JSON).body("{not json")
                .when().post("/api/v1/examples")
                .then().statusCode(400).body("error.code", equalTo("INVALID_ARGUMENT"));
    }

    @Test
    void unknownResourceReturns404() {
        given().when().get("/api/v1/examples/999")
                .then().statusCode(404);
    }
}

package com.forgebase.quarkus;

import io.quarkus.test.junit.QuarkusTest;
import io.restassured.http.ContentType;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;
import static org.hamcrest.Matchers.equalTo;

@QuarkusTest
class ApplicationTests {

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
    void createReturnsEnvelope() {
        given().contentType(ContentType.JSON).body("{\"name\":\"first\"}")
                .when().post("/api/v1/examples")
                .then().statusCode(201).body("data.id", equalTo(1)).body("data.name", equalTo("first"));
    }

    @Test
    void blankNameIsRejected() {
        given().contentType(ContentType.JSON).body("{\"name\":\"\"}")
                .when().post("/api/v1/examples")
                .then().statusCode(400);
    }

    @Test
    void unknownResourceReturns404() {
        given().when().get("/api/v1/examples/999")
                .then().statusCode(404);
    }
}

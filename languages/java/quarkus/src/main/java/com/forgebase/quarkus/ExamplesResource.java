package com.forgebase.quarkus;

import jakarta.inject.Inject;
import jakarta.ws.rs.*;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.core.Response;

import java.util.List;
import java.util.Map;

@Path("/api/v1/examples")
@Produces(MediaType.APPLICATION_JSON)
@Consumes(MediaType.APPLICATION_JSON)
public class ExamplesResource {

    @Inject
    ExampleService service;

    @POST
    public Response create(CreateRequest request) {
        // Manual validation keeps the resource free of bean-validation quirks
        // while still failing fast with a 400 on bad input.
        if (request == null || request.name() == null || request.name().isBlank()) {
            return Response.status(400).entity(Map.of("error", Map.of("code", "INVALID_ARGUMENT", "message", "name must not be empty"))).build();
        }
        return Response.status(201).entity(Map.of("data", service.create(request.name()), "message", "created")).build();
    }

    @GET
    public List<Example> list() {
        return service.list();
    }

    @GET
    @Path("/{id}")
    public Example get(@PathParam("id") int id) {
        return service.get(id);
    }

    public record CreateRequest(String name) {
    }
}

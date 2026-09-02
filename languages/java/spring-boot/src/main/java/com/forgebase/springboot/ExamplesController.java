package com.forgebase.springboot;

import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.Size;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/v1/examples")
public class ExamplesController {
    private final ExampleService service;

    public ExamplesController(ExampleService service) {
        this.service = service;
    }

    @PostMapping
    public ResponseEntity<Example> create(@Valid @RequestBody CreateRequest request) {
        return ResponseEntity.status(201).body(service.create(request.name()));
    }

    @GetMapping
    public List<Example> list() {
        return service.list();
    }

    @GetMapping("/{id}")
    public Example get(@PathVariable int id) {
        return service.get(id);
    }

    public record CreateRequest(@NotBlank @Size(max = 100) String name) {
    }
}

package com.forgebase.springboot;

import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * Example service — framework-free, in-memory, unit-testable.
 * Deliberately generic.
 */
@Service
public class ExampleService {
    private final AtomicInteger nextId = new AtomicInteger(1);
    private final List<Example> items = new ArrayList<>();

    public Example create(String name) {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("name must not be empty");
        }
        Example example = new Example(nextId.getAndIncrement(), name.trim());
        items.add(example);
        return example;
    }

    public Example get(int id) {
        return items.stream()
                .filter(item -> item.id() == id)
                .findFirst()
                .orElseThrow(() -> DomainError.notFound("Example " + id + " not found"));
    }

    public List<Example> list() {
        return List.copyOf(items);
    }
}

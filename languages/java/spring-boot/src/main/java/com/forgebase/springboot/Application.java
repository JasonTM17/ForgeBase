package com.forgebase.springboot;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.boot.context.properties.ConfigurationPropertiesScan;
import org.springframework.validation.annotation.Validated;

/**
 * Application entry point with fail-fast, validated configuration bound to the
 * {@code app.*} prefix in application.yml.
 */
@SpringBootApplication
@ConfigurationPropertiesScan
public class Application {
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
    }
}

@ConfigurationProperties(prefix = "app")
@Validated
record AppProps(String env) {
    AppProps {
        if (env == null || env.isBlank()) {
            throw new IllegalArgumentException("app.env is required");
        }
    }
}

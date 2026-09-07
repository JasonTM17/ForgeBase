package com.forgebase.quarkus;

import java.util.Locale;

import io.quarkus.logging.Log;
import io.quarkus.runtime.StartupEvent;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.Observes;
import jakarta.inject.Inject;

/**
 * Consumes the validated configuration on startup: the name and environment
 * feed the startup log line so every deployment is traceable to its
 * configuration.
 */
@ApplicationScoped
public class ApplicationLifecycle {

    private final AppConfig config;

    @Inject
    ApplicationLifecycle(AppConfig config) {
        this.config = config;
    }

    void onStart(@Observes StartupEvent event) {
        Log.infof("starting service %s in %s",
                config.name(), config.env().name().toLowerCase(Locale.ROOT));
    }
}

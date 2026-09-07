package com.forgebase.quarkus;

import io.smallrye.config.ConfigMapping;

/**
 * Fail-fast application configuration. Values are expanded from the
 * environment through application.properties and bound at startup: an
 * APP_ENV value outside the enum aborts boot with a configuration error
 * instead of degrading at request time.
 */
@ConfigMapping(prefix = "forgebase.app")
public interface AppConfig {

    String name();

    AppEnv env();

    enum AppEnv {
        DEVELOPMENT, TESTING, PRODUCTION
    }
}

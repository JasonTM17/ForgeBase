/* setenv/unsetenv are POSIX; expose them under strict -std=c11. */
#if !defined(_WIN32)
#define _POSIX_C_SOURCE 200809L
#endif

#include "starter/config.h"
#include "starter/greeter.h"
#include "starter/logging.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Dependency-free test binary registered with CTest. CHECK records the
 * failing test and line, then stops the binary with a non-zero exit. */
static int failures = 0;

#define CHECK(condition)                                                       \
    do {                                                                       \
        if (!(condition)) {                                                    \
            fprintf(stderr, "FAIL %s:%d: %s\n", __func__, __LINE__, #condition); \
            failures++;                                                        \
            return;                                                            \
        }                                                                      \
    } while (0)

static void test_log_severity_parses_known_names(void)
{
    CHECK(starter_log_severity_parse("critical") == STARTER_LOG_CRITICAL);
    CHECK(starter_log_severity_parse("Information") == STARTER_LOG_INFORMATION);
    CHECK(starter_log_severity_parse("TRACE") == STARTER_LOG_TRACE);
}

static void test_log_severity_rejects_unknown(void)
{
    CHECK(starter_log_severity_parse("loud") == -1);
    CHECK(starter_log_severity_parse("") == -1);
    CHECK(starter_log_severity_parse(NULL) == -1);
}

static void test_config_requires_service_name(void)
{
    unsetenv("SERVICE_NAME");

    starter_config_t config;
    char *error = NULL;
    CHECK(starter_config_from_environment(&config, &error) == -1);
    CHECK(error != NULL && strstr(error, "SERVICE_NAME") != NULL);
    starter_error_free(&error);
}

static void test_config_defaults_log_level(void)
{
    setenv("SERVICE_NAME", "demo", 1);
    unsetenv("APP_LOG_LEVEL");

    starter_config_t config;
    char *error = NULL;
    CHECK(starter_config_from_environment(&config, &error) == 0);
    CHECK(strcmp(config.service_name, "demo") == 0);
    CHECK(config.log_level == STARTER_LOG_INFORMATION);
    starter_error_free(&error);
}

static void test_config_rejects_unknown_level(void)
{
    setenv("SERVICE_NAME", "demo", 1);
    setenv("APP_LOG_LEVEL", "loud", 1);

    starter_config_t config;
    char *error = NULL;
    CHECK(starter_config_from_environment(&config, &error) == -1);
    CHECK(error != NULL && strstr(error, "APP_LOG_LEVEL") != NULL);
    starter_error_free(&error);
}

static void test_greeter_greets_and_rejects_empty(void)
{
    char buffer[128];
    CHECK(starter_greeter_greet("ForgeBase", buffer, sizeof(buffer)) == 0);
    CHECK(strcmp(buffer, "Hello, ForgeBase!") == 0);
    CHECK(starter_greeter_greet("   ", buffer, sizeof(buffer)) == -1);
    CHECK(starter_greeter_greet("ForgeBase", buffer, 8) == -1);
}

int main(void)
{
    test_log_severity_parses_known_names();
    test_log_severity_rejects_unknown();
    test_config_requires_service_name();
    test_config_defaults_log_level();
    test_config_rejects_unknown_level();
    test_greeter_greets_and_rejects_empty();

    if (failures > 0) {
        fprintf(stderr, "%d check(s) failed\n", failures);
        return 1;
    }
    printf("all starter tests passed\n");
    return 0;
}

#include "starter/config.h"

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static const char *config_required(const char *name, char **error)
{
    const char *value = getenv(name);
    if (value == NULL || value[0] == '\0') {
        if (*error == NULL) {
            size_t needed = (size_t)snprintf(NULL, 0,
                "required environment variable %s is missing or empty", name);
            *error = malloc(needed + 1);
            snprintf(*error, needed + 1,
                "required environment variable %s is missing or empty", name);
        }
        return NULL;
    }
    return value;
}

void starter_error_free(char **error)
{
    if (error != NULL && *error != NULL) {
        free(*error);
        *error = NULL;
    }
}

int starter_config_from_environment(starter_config_t *out, char **error)
{
    *error = NULL;

    const char *service_name = config_required("SERVICE_NAME", error);
    if (service_name == NULL) {
        return -1;
    }

    const char *level = getenv("APP_LOG_LEVEL");
    if (level == NULL || level[0] == '\0') {
        level = "information";
    }
    int parsed = starter_log_severity_parse(level);
    if (parsed < 0) {
        if (*error == NULL) {
            static const char message[] =
                "APP_LOG_LEVEL is invalid. Valid values: critical, error, "
                "warning, information, debug, trace.";
            *error = malloc(sizeof(message));
            memcpy(*error, message, sizeof(message));
        }
        return -1;
    }

    out->service_name = service_name;
    out->log_level = (starter_log_severity_t)parsed;
    return 0;
}

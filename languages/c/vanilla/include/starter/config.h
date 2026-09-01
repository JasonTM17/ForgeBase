#ifndef STARTER_CONFIG_H
#define STARTER_CONFIG_H

#include "starter/log_severity.h"

/* Fail-fast configuration: missing required variables or values that fail
 * validation abort startup before any real work happens. */
typedef struct {
    const char *service_name;
    starter_log_severity_t log_level;
} starter_config_t;

/* Reads the process environment. Returns 0 and fills *out on success;
 * returns -1 and writes a human-readable reason into *error on failure.
 * error must be released with starter_error_free(). */
int starter_config_from_environment(starter_config_t *out, char **error);

/* Releases an error string allocated by starter_config_from_environment(). */
void starter_error_free(char **error);

#endif /* STARTER_CONFIG_H */

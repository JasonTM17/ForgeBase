#ifndef STARTER_LOGGING_H
#define STARTER_LOGGING_H

#include "starter/log_severity.h"

/* Minimal leveled logger: ISO-8601 UTC timestamp, severity tag, and service
 * context on every line. Errors go to stderr. */
typedef struct {
    starter_log_severity_t threshold;
    const char *service;
} starter_logger_t;

void starter_logger_init(starter_logger_t *logger,
                         starter_log_severity_t threshold,
                         const char *service);
void starter_logger_log(const starter_logger_t *logger,
                        starter_log_severity_t severity,
                        const char *message);

#endif /* STARTER_LOGGING_H */

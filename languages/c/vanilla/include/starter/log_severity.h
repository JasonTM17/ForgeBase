#ifndef STARTER_LOG_SEVERITY_H
#define STARTER_LOG_SEVERITY_H

/* Severity levels for the built-in console logger, ordered from most to
 * least severe. The integer order is the severity order. */
typedef enum {
    STARTER_LOG_CRITICAL = 0,
    STARTER_LOG_ERROR = 1,
    STARTER_LOG_WARNING = 2,
    STARTER_LOG_INFORMATION = 3,
    STARTER_LOG_DEBUG = 4,
    STARTER_LOG_TRACE = 5
} starter_log_severity_t;

/* Parses a case-insensitive level name; returns -1 when unknown. */
int starter_log_severity_parse(const char *name);

#endif /* STARTER_LOG_SEVERITY_H */

/* gmtime_r is POSIX; exposing it under strict -std=c11 (extensions off)
 * requires the feature-test macro before any include. */
#if !defined(_WIN32)
#define _POSIX_C_SOURCE 200809L
#endif

#include "starter/logging.h"

#include <stdio.h>
#include <string.h>
#include <time.h>

void starter_logger_init(starter_logger_t *logger,
                         starter_log_severity_t threshold,
                         const char *service)
{
    logger->threshold = threshold;
    logger->service = service;
}

void starter_logger_log(const starter_logger_t *logger,
                        starter_log_severity_t severity,
                        const char *message)
{
    if (severity > logger->threshold) {
        return;
    }

    static const char *tags[] = { "CRI", "ERR", "WAR", "INF", "DEB", "TRA" };

    char timestamp[32];
    time_t now = time(NULL);
    struct tm utc;
#ifdef _WIN32
    gmtime_s(&utc, &now);
#else
    gmtime_r(&now, &utc);
#endif
    strftime(timestamp, sizeof(timestamp), "%Y-%m-%dT%H:%M:%SZ", &utc);

    FILE *sink = severity <= STARTER_LOG_ERROR ? stderr : stdout;
    fprintf(sink, "%s [%s] service=%s %s\n",
            timestamp, tags[severity], logger->service, message);
}

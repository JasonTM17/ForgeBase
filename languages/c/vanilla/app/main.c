#include "starter/config.h"
#include "starter/greeter.h"
#include "starter/logging.h"

#include <stdio.h>
#include <stdlib.h>

/* Fail-fast demo: a missing or invalid configuration variable exits with a
 * clean message and a non-zero code instead of a stack trace. */
int main(void)
{
    starter_config_t config;
    char *error = NULL;
    if (starter_config_from_environment(&config, &error) != 0) {
        fprintf(stderr, "configuration error: %s\n", error);
        starter_error_free(&error);
        return 2;
    }

    starter_logger_t logger;
    starter_logger_init(&logger, config.log_level, config.service_name);
    starter_logger_log(&logger, STARTER_LOG_INFORMATION, "service starting");

    char greeting[128];
    if (starter_greeter_greet("ForgeBase", greeting, sizeof(greeting)) != 0) {
        starter_logger_log(&logger, STARTER_LOG_ERROR, "greeting failed");
        return 1;
    }
    printf("%s\n", greeting);

    starter_logger_log(&logger, STARTER_LOG_INFORMATION, "service finished");
    return 0;
}

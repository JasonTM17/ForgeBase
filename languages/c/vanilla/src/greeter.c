#include "starter/greeter.h"

#include <ctype.h>
#include <stdio.h>

int starter_greeter_greet(const char *name, char *buffer, size_t buffer_size)
{
    if (name == NULL || buffer == NULL) {
        return -1;
    }

    /* Reject empty or whitespace-only names, matching the trim semantics of
     * the other vanilla starters. */
    int has_content = 0;
    for (const char *cursor = name; *cursor != '\0'; cursor++) {
        if (!isspace((unsigned char)*cursor)) {
            has_content = 1;
            break;
        }
    }
    if (!has_content) {
        return -1;
    }

    int written = snprintf(buffer, buffer_size, "Hello, %s!", name);
    if (written < 0 || (size_t)written >= buffer_size) {
        return -1;
    }
    return 0;
}

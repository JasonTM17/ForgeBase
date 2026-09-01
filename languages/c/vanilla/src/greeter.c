#include "starter/greeter.h"

#include <stdio.h>
#include <string.h>

int starter_greeter_greet(const char *name, char *buffer, size_t buffer_size)
{
    if (name == NULL || buffer == NULL || name[0] == '\0') {
        return -1;
    }

    int written = snprintf(buffer, buffer_size, "Hello, %s!", name);
    if (written < 0 || (size_t)written >= buffer_size) {
        return -1;
    }
    return 0;
}

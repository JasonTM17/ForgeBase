#include "starter/log_severity.h"

#include <ctype.h>
#include <string.h>

int starter_log_severity_parse(const char *name)
{
    static const char *names[] = {
        "critical", "error", "warning", "information", "debug", "trace"
    };
    static const int count = (int)(sizeof(names) / sizeof(names[0]));

    if (name == NULL) {
        return -1;
    }

    char lowered[32];
    size_t length = strlen(name);
    if (length == 0 || length >= sizeof(lowered)) {
        return -1;
    }
    for (size_t i = 0; i < length; i++) {
        lowered[i] = (char)tolower((unsigned char)name[i]);
    }
    lowered[length] = '\0';

    for (int i = 0; i < count; i++) {
        if (strcmp(lowered, names[i]) == 0) {
            return i;
        }
    }
    return -1;
}

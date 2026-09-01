#ifndef STARTER_GREETER_H
#define STARTER_GREETER_H

#include <stddef.h>

/* Example domain service. It exists to demonstrate the shape a real service
 * takes (validation -> behavior), not to carry business meaning — replace
 * it when copying the template out. */

/* Writes "Hello, <name>!" into buffer. Returns 0 on success, -1 when name
 * is empty and buffer_size is too small. */
int starter_greeter_greet(const char *name, char *buffer, size_t buffer_size);

#endif /* STARTER_GREETER_H */

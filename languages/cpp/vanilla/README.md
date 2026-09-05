# C++ Vanilla Starter

A zero-dependency C++20 library + CLI base: CMake build with warnings-as-
errors, fail-fast environment configuration, leveled UTC-timestamped
logging, an example domain service, and CTest-registered tests. Standard
library only — the template fits libraries, tools, and services before any
third-party choice is made.

## Features

- Fail-fast `Config::from_environment` with a dedicated `config_error`
  exception type (clean exit instead of a half-initialized runtime)
- Leveled `Logger` class with ISO-8601 UTC timestamps (errors on stderr)
- Example service with input validation and exception-based error contract
- CTest integration; `-Wall -Wextra -Werror` on every target

## Requirements

- C++20 compiler and CMake >= 3.24 (verified with GCC 14 in the official
  `gcc:14-bookworm` container image; MSVC warning flags are supported too)

## Project structure

```text
vanilla/
├── CMakeLists.txt
├── include/starter/        # public API surface
│   ├── config.hpp          # fail-fast environment configuration
│   ├── log_severity.hpp    # severity enum + case-insensitive parsing
│   ├── logging.hpp
│   └── greeter.hpp
├── src/                    # implementation
├── app/main.cpp            # CLI demo (clean fail-fast exit)
└── tests/test_starter.cpp  # tests, registered with CTest
```

## Getting started

Copy this folder out and rename:

```bash
cp -r languages/cpp/vanilla /path/to/my-project
cd /path/to/my-project
# rename the "starter" targets and the starter namespace
cmake -S . -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
ctest --test-dir build --output-on-failure
./build/starter_cli
```

## Configuration

| Variable | Required | Default | Meaning |
|---|---|---|---|
| `SERVICE_NAME` | yes | — | service identity used in log lines |
| `APP_LOG_LEVEL` | no | `information` | one of `critical`, `error`, `warning`, `information`, `debug`, `trace` (case-insensitive) |

Missing or invalid values abort startup with exit code `2` and a clean
message — no stack trace.

## Running

```bash
SERVICE_NAME=demo ./build/starter_cli
```

## Testing

```bash
ctest --test-dir build --output-on-failure
```

## Linting / formatting

The template compiles with `-Wall -Wextra -Werror`. Add clang-format
(`.clang-format` with the LLVM or Google style) and clang-tidy when the
copied-out project grows a style guide.

## Docker

Not applicable: this starter is a library/CLI base with no runtime service.
Repository-level verification runs inside the `gcc:14-bookworm` image; add a
Dockerfile when the copied-out project ships a server component.

## Production notes

- The severity order is carried by the enumerator order; string parsing is
  centralized in `parse_log_severity`.
- `config_error` lets hosts map configuration failures to their own exit
  semantics; nothing else throws across the library boundary.
- UTC conversion and test environment setup use platform-specific APIs so
  strict C++20 builds remain warning-clean on POSIX and Windows hosts.

## Common issues

- **`cmake` not installed on the host** — the repository verifies in Docker;
  locally, install CMake >= 3.24 or use the container workflow.
- **`gmtime` conversion fails to compile** — keep the `_WIN32` branch in the
  logger and use a C++20-capable compiler selected by CMake.

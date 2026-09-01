# C Vanilla Starter

A zero-dependency C11 library + CLI base: CMake build with warnings-as-
errors, fail-fast environment configuration, leveled UTC-timestamped
logging, an example domain service, and CTest-registered assert-based
tests. No runtime dependencies — the template fits libraries, tools, and
embedded-adjacent projects before any third-party choice is made.

## Features

- Fail-fast `starter_config_from_environment`: clean error string + exit
  path instead of half-initialized runtime
- Leveled logger with ISO-8601 UTC timestamps (errors on stderr)
- Example service with input validation and explicit error returns
- CTest integration; `-Wall -Wextra -Werror` on every target

## Requirements

- C11 compiler and CMake >= 3.24 (verified with gcc 14 in the official
  `gcc:14-bookworm` container image)

## Project structure

```text
vanilla/
├── CMakeLists.txt
├── include/starter/        # public API surface
│   ├── config.h            # fail-fast environment configuration
│   ├── log_severity.h      # severity enum + case-insensitive parsing
│   ├── logging.h
│   └── greeter.h
├── src/                    # implementation
├── app/main.c              # CLI demo (clean fail-fast exit)
└── tests/test_starter.c    # assert-based tests, registered with CTest
```

## Getting started

Copy this folder out and rename:

```bash
cp -r languages/c/vanilla /path/to/my-project
cd /path/to/my-project
# rename the "starter" targets and the starter_ header prefix
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
(`.clang-format` with the LLVM or Google style) when the copied-out project
grows a style guide.

## Docker

Not applicable: this starter is a library/CLI base with no runtime service.
Repository-level verification runs inside the `gcc:14-bookworm` image; add a
Dockerfile when the copied-out project ships a server component.

## Production notes

- Configuration errors are returned as a heap-allocated message owned by
  the caller (`starter_error_free`) — no globals, no hidden state.
- The static library has no runtime dependencies beyond libc, so it links
  cleanly into larger projects.
- Buffer-size contracts (`starter_greeter_greet`) keep the example safe to
  copy into constrained environments.

## Common issues

- **`cmake` not installed on the host** — the repository verifies in Docker;
  locally, install CMake >= 3.24 or use the container workflow.
- **Windows line endings in tests** — keep LF; the repository's
  `.gitattributes` enforces it.

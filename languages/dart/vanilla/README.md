# Dart Vanilla Starter

A zero-dependency Dart 3.3+ library/CLI base: fail-fast environment
configuration, leveled console logging with UTC timestamps, an example
domain service, and a `dart test` suite. Standard library only.

## Features

- Fail-fast `EnvConfig.fromEnvironment` with a dedicated `EnvConfigError`
- `LogSeverity` enum whose declaration order is the severity order
- `ConsoleLogger` with ISO-8601 UTC timestamps (errors on stderr)
- `dart test` suite covering config, severity ordering, and the example
  service

## Requirements

- Dart SDK >= 3.3 (verified in the official `dart:3.9` container image)

## Project structure

```text
vanilla/
├── pubspec.yaml
├── bin/starter.dart            # CLI demo (clean fail-fast exit)
├── lib/
│   └── src/
│       ├── config.dart         # fail-fast environment configuration
│       ├── log_severity.dart   # severity enum + parsing
│       ├── console_logger.dart # leveled timestamped logging
│       └── greeter.dart        # example domain service
└── test/starter_test.dart
```

## Getting started

Copy this folder out and rename:

```bash
cp -r languages/dart/vanilla /path/to/my-project
cd /path/to/my-project
# rename the package in pubspec.yaml
dart test
```

## Configuration

| Variable | Required | Default | Meaning |
|---|---|---|---|
| `SERVICE_NAME` | yes | — | service identity used in log lines |
| `APP_LOG_LEVEL` | no | `information` | one of `critical`, `error`, `warning`, `information`, `debug`, `trace` (case-insensitive) |

Missing or invalid values abort with exit code `2` and a clean message —
no stack trace.

## Running

```bash
SERVICE_NAME=dart dart run bin/starter.dart
```

## Testing

```bash
dart test
```

## Linting / formatting

```bash
dart analyze
dart format --output=none --set-exit-if-changed .
```

## Docker

Not applicable: this starter is a library/CLI base with no runtime service.
Repository-level verification runs inside the `dart:3.9` image; add a
Dockerfile when the copied-out project grows a server component.

## Production notes

- Configuration errors surface as `EnvConfigError` so hosts can map them to
  their own exit semantics.
- `LogSeverity` ordering follows the enum declaration order; never sort
  severity names alphabetically.
- The local logger is dependency-free; swap in `logging` when you need
  hierarchical loggers.

## Common issues

- **`dart` not installed on the host** — the repository verifies in Docker;
  locally, install the Dart SDK or use the container workflow.
- **Pub dependencies** — `dart test` runs `dart pub get` automatically; the
  only dev dependency is the `test` package.

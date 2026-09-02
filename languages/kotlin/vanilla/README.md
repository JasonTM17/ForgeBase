# Kotlin Vanilla Starter

A zero-dependency Kotlin library/CLI base: Gradle Kotlin DSL, JDK 21
toolchain, fail-fast environment configuration, leveled console logging
with UTC timestamps, an example domain service, and kotlin.test tests.
No runtime dependencies beyond the Kotlin standard library.

## Features

- Fail-fast `EnvConfig.fromEnvironment` with a dedicated
  `EnvConfigException`
- `LogSeverity` enum whose declaration order is the severity order
  (`compareTo` stays correct without manual ranks)
- `ConsoleLogger` with ISO-8601 UTC timestamps (errors on stderr)
- kotlin.test suite with JUnit Platform

## Requirements

- JDK 21 (verified in the official `gradle:8.14-jdk21` container image)
- Gradle (the Kotlin DSL is verified with Gradle 8.14)

## Project structure

```text
vanilla/
├── settings.gradle.kts
├── build.gradle.kts
└── src/
    ├── main/kotlin/
    │   ├── starter/
    │   │   ├── EnvConfig.kt       # fail-fast environment configuration
    │   │   ├── LogSeverity.kt     # severity enum + parsing
    │   │   ├── ConsoleLogger.kt   # leveled timestamped logging
    │   │   └── Greeter.kt         # example domain service
    │   └── Main.kt                # CLI demo (clean fail-fast exit)
    └── test/kotlin/starter/StarterTest.kt
```

## Getting started

Copy this folder out and rename:

```bash
cp -r languages/kotlin/vanilla /path/to/my-project
cd /path/to/my-project
# rename the project in settings.gradle.kts and the starter package
gradle run
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
SERVICE_NAME=demo gradle run
```

## Testing

```bash
gradle test
```

## Linting / formatting

The starter carries no formatter dependency. Common additions after copying
out: ktlint or Spotless with `formatKotlin`. Keep the Kotlin coding
conventions (the sources here follow them).

## Docker

Not applicable: this starter is a library/CLI base with no runtime service.
Repository-level verification runs inside the `gradle:8.14-jdk21` image; add
a Dockerfile when the copied-out project grows a server component.

## Production notes

- Configuration errors surface as `EnvConfigException` so hosts can map
  them to their own exit semantics.
- The application plugin's `mainClass` points at `starter.MainKt`; update
  it when renaming the package.
- `jvmToolchain(21)` keeps builds reproducible across machines.

## Common issues

- **`gradle` not installed on the host** — the repository verifies in
  Docker; locally, use a Gradle wrapper (`gradle wrapper`) to pin the
  version.
- **Tests not discovered** — `useJUnitPlatform()` in `build.gradle.kts` is
  required for kotlin.test; keep it.

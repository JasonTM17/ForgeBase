# C# Vanilla Starter

A zero-dependency C# library/CLI base: fail-fast environment configuration,
structured console logging with timestamps and severity, an example domain
service, and xunit tests. Deliberately free of frameworks so it fits library,
tool, and CLI projects before any dependency is chosen.

## Features

- Fail-fast `EnvConfig`: startup aborts with a clean message on missing or
  invalid environment variables
- Leveled `ConsoleLogger` with ISO-8601 timestamps and service context
  (errors on stderr, everything else on stdout)
- Example domain service with input validation (the pattern real services
  follow)
- xunit test suite with `TreatWarningsAsErrors` and nullable reference types
  enabled

## Requirements

- .NET SDK 8.0 or newer (verified with SDK 8.0.424)

## Project structure

```text
vanilla/
├── Starter.sln
├── src/Starter/            # library + CLI entry point
│   ├── Program.cs          # top-level CLI demo with clean fail-fast exit
│   ├── EnvConfig.cs        # fail-fast environment configuration
│   ├── LogSeverity.cs      # local severity enum (zero dependencies)
│   ├── ConsoleLogger.cs    # leveled timestamped console logging
│   └── Greeter.cs          # example domain service
└── tests/Starter.Tests/    # xunit tests for config + service
```

## Getting started

Copy this folder out and rename:

```bash
cp -r languages/csharp/vanilla /path/to/my-project
cd /path/to/my-project
# rename the solution and projects from "Starter" to your product name
dotnet build
dotnet test
dotnet run --project src/Starter
```

## Configuration

| Variable | Required | Default | Meaning |
|---|---|---|---|
| `SERVICE_NAME` | yes | — | service identity used in log lines |
| `APP_LOG_LEVEL` | no | `Information` | one of `Critical`, `Error`, `Warning`, `Information`, `Debug`, `Trace` (case-insensitive) |

Missing or invalid values abort startup with exit code `2` and a clean
message — no stack trace.

## Running

```bash
SERVICE_NAME=demo dotnet run --project src/Starter
```

## Testing

```bash
dotnet test
```

## Linting / formatting

```bash
dotnet format --verify-no-changes
```

Style rules live in `.editorconfig` (file-scoped namespaces, UTF-8, LF).

## Docker

Not applicable: this starter is a library/CLI base with no runtime service.
Add a Dockerfile when the copied-out project grows a server component.

## Production notes

- `TreatWarningsAsErrors` keeps compiler warnings from accumulating silently.
- The local `LogSeverity`/`ConsoleLogger` pair is intentionally dependency
  free; swap in a structured logging library when you need JSON sinks without
  changing call sites (both are behind small types).
- Configuration errors are surfaced as `EnvConfigException` so hosts can map
  them to their own exit semantics.

## Common issues

- **`dotnet format` complains on first run** — ensure LF line endings are
  checked out (the repository's `.gitattributes` enforces this).
- **Build warnings become errors** — that is deliberate; fix the warning or
  downgrade the specific diagnostic in `.editorconfig`.

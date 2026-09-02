# Ruby Vanilla Starter

A zero-dependency Ruby 3.3+ library/CLI base: fail-fast environment
configuration, leveled console logging with UTC timestamps, an example
domain service, and a minitest suite. `Data`-based immutable config, no
runtime gems.

## Features

- Fail-fast `Starter.load_config` with a dedicated `EnvConfigError`
- Immutable `EnvConfig` value object (`Data.define`)
- `LogSeverity` with correct severity ordering (`Comparable` — string
  comparisons would order alphabetically)
- `ConsoleLogger` with ISO-8601 UTC timestamps (errors on stderr)
- minitest suite covering config, severity ordering, and the example service

## Requirements

- Ruby >= 3.3 (verified in the official `ruby:3.3` container image)

## Project structure

```text
vanilla/
├── bin/starter                 # executable CLI demo (clean fail-fast exit)
├── lib/
│   ├── starter.rb              # gem entrypoint (requires all modules)
│   └── starter/
│       ├── config.rb           # fail-fast environment configuration
│       ├── log_severity.rb     # severity ordering + parsing
│       ├── console_logger.rb   # leveled timestamped logging
│       └── greeter.rb          # example domain service
└── test/run_test.rb            # minitest suite
```

## Getting started

Copy this folder out and rename:

```bash
cp -r languages/ruby/vanilla /path/to/my-project
cd /path/to/my-project
# rename the Starter module and the gem identity
ruby bin/starter
ruby test/run_test.rb
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
SERVICE_NAME=demo ruby bin/starter
```

## Testing

```bash
ruby test/run_test.rb
```

## Linting / formatting

The starter carries no formatter dependency. Common additions after copying
out: StandardRB or RuboCop. Source code follows frozen-string-literal and
2-space indentation conventions.

## Docker

Not applicable: this starter is a library/CLI base with no runtime service.
Repository-level verification runs inside the `ruby:3.3` image; add a
Dockerfile when the copied-out project grows a server component.

## Production notes

- `LogSeverity` implements `Comparable` over an explicit rank; never sort
  severity names alphabetically.
- Configuration errors surface as `EnvConfigError` so hosts can map them to
  their own exit semantics.
- Add a `.gemspec` when the copied-out project should ship as a gem.

## Common issues

- **`bin/starter` not executable** — run `chmod +x bin/starter` on
  Unix-like systems after copying out.
- **`Data` undefined on old rubies** — `Data` requires Ruby 3.2+; the
  starter's floor is 3.3.

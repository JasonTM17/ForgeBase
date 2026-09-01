# PHP Vanilla Starter

A zero-dependency PHP 8.3+ library/CLI base: composer PSR-4 autoload,
fail-fast environment configuration, leveled console logging with UTC
timestamps, an example domain service, and a dependency-free test runner.
No runtime packages — the template works before the first
`composer install` and stays clean when you add your own.

## Features

- Fail-fast `EnvConfig`: startup aborts with a clean message on missing or
  invalid environment variables
- Leveled `ConsoleLogger` with ISO-8601 UTC timestamps (errors on stderr)
- Backed enum severity levels with an explicit rank (string enums must not
  be compared alphabetically)
- `bootstrap.php` dual autoloader: composer's autoloader when present, a
  PSR-4 fallback otherwise
- Dependency-free test runner with a PHPUnit-shaped exit contract
  (non-zero on failure)

## Requirements

- PHP 8.3 or newer (verified with PHP 8.5.4 CLI)
- Composer (optional; only the autoloader changes with no dependencies)

## Project structure

```text
vanilla/
├── bin/starter             # executable CLI demo (clean fail-fast exit)
├── bootstrap.php           # dual autoloader (composer or PSR-4 fallback)
├── composer.json           # forgebase/starter, PSR-4, "test" script
├── src/
│   ├── EnvConfig.php       # fail-fast environment configuration
│   ├── EnvConfigException.php
│   ├── LogSeverity.php     # backed enum + severity rank
│   ├── ConsoleLogger.php   # leveled timestamped logging
│   └── Greeter.php         # example domain service
└── tests/
    ├── run.php             # zero-dependency runner
    ├── bootstrap.php
    ├── Support.php         # expect_* helpers
    ├── EnvConfigTest.php
    └── GreeterTest.php
```

## Getting started

Copy this folder out and rename:

```bash
cp -r languages/php/vanilla /path/to/my-project
cd /path/to/my-project
# rename the forgebase/starter package and the ForgeBase\Starter namespace
composer install   # optional; dumps the real autoloader
php tests/run.php
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
php bin/starter                      # uses the current environment
SERVICE_NAME=demo php bin/starter
```

## Testing

```bash
php tests/run.php        # or: composer test
```

## Linting / formatting

The starter carries no formatter dependency. Common additions after copying
out: `php-cs-fixer` or `phpcbf`/`phpcs` (PSR-12). Source code already
follows PSR-12 layout, strict types, and final classes.

## Docker

Not applicable: this starter is a library/CLI base with no runtime service.
Repository-level verification uses the official `composer:2` and
`php:8.3-cli` images; add a Dockerfile when the copied-out project grows a
server component.

## Production notes

- The local severity enum/logger pair is intentionally dependency free;
  swap in Monolog or similar when you need structured sinks — call sites
  stay small because both types are final and local.
- `declare(strict_types=1)` is used everywhere; keep it that way in the
  copied-out project.
- Configuration errors surface as `EnvConfigException` so hosts can map
  them to their own exit semantics.

## Common issues

- **`bin/starter` not executable** — run `chmod +x bin/starter` after
  copying out on Unix-like systems.
- **Autoloader seems stale** — after renaming namespaces, run
  `composer dump-autoload` or clear opcache.

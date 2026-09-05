# PHP Laravel Starter

Production-oriented **Laravel 13 REST API base**: framework-idiomatic routing,
fail-fast environment configuration, centralized JSON errors, `/up` health,
example API resource, PHPUnit tests, and a non-root Docker image.

## Features

- Laravel 13 skeleton kept idiomatic and copy-out friendly
- Environment-driven configuration with safe defaults in `.env.example`
- JSON API route group under `/api`
- Centralized JSON rendering for API exceptions
- `GET /up` health endpoint using Laravel's built-in health route
- Example resource at `/api/examples`
- PHPUnit unit and feature tests for service logic, health, and API behavior
- Multi-stage Dockerfile with Composer install and a non-root runtime user

## Requirements

- PHP >= 8.4.1 with the Laravel-required extensions
- Composer 2+
- Node.js >= 22 only if you keep the optional Vite frontend assets
- Docker 24+ for container builds

## Project structure

```text
laravel/
├── app/
│   ├── Http/Controllers/ExampleController.php
│   ├── Providers/AppServiceProvider.php
│   └── Services/ExampleService.php
├── bootstrap/app.php
├── config/
├── routes/
│   ├── api.php
│   ├── console.php
│   └── web.php
├── tests/
│   ├── Feature/ExampleApiTest.php
│   └── Unit/ExampleServiceTest.php
├── .env.example
├── Dockerfile
├── .dockerignore
├── composer.json
└── forgebase.json
```

## Getting started

Copy this folder out and rename the Composer package/application identity:

```bash
cp -r languages/php/laravel /path/to/my-api
cd /path/to/my-api
cp .env.example .env
composer install
php artisan key:generate
php artisan serve --host=0.0.0.0 --port=8000
```

## Configuration

| Variable            | Required | Default                 | Meaning |
| ------------------- | -------- | ----------------------- | ------- |
| `APP_NAME`          | no       | `ForgeBase Laravel`     | Application name |
| `APP_ENV`           | no       | `local`                 | Laravel environment |
| `APP_KEY`           | yes      | empty in example        | Laravel encryption key; generate after copying out |
| `APP_DEBUG`         | no       | `false`                 | Enables framework debug output outside production |
| `APP_URL`           | no       | `http://localhost:8000` | Base URL used by console-generated links |
| `LOG_CHANNEL`       | no       | `stack`                 | Laravel log channel |
| `LOG_LEVEL`         | no       | `info`                  | Minimum log level |
| `CACHE_STORE`       | no       | `array`                 | Cache store for this dependency-light starter |
| `QUEUE_CONNECTION`  | no       | `sync`                  | Queue driver |
| `SESSION_DRIVER`    | no       | `array`                 | Session driver |
| `DB_CONNECTION`     | no       | `sqlite`                | Database driver if you add persistence |

Phase 1 keeps persistence out of scope. The default test/runtime settings avoid
external database, queue, and cache services.

## Running

```bash
php artisan serve --host=0.0.0.0 --port=8000
curl http://localhost:8000/up
curl http://localhost:8000/api/examples
```

Production-style run after installing dependencies:

```bash
php artisan config:cache
php artisan route:cache
php artisan serve --host=0.0.0.0 --port=8000
```

## Testing

```bash
composer test
# or
php artisan test
```

The tests cover service validation, `/up`, root envelope output, example API
listing, and validation errors without stack-trace fields.

## Linting / formatting

```bash
vendor/bin/pint --test
vendor/bin/pint
```

Pint is installed through Laravel's dev dependencies after `composer install`.

## Docker

```bash
docker build -t my-laravel-api .
docker run --rm -p 8000:8000 --env-file .env my-laravel-api
```

The runtime stage installs production Composer dependencies, prepares writable
Laravel cache/storage directories, and runs as a non-root `app` user.

## Production notes

- Generate a real `APP_KEY` after copying out; never commit a generated key.
- Keep API error responses JSON-only for `/api/*` routes so stack traces and
  internal exception details are not exposed.
- Add database migrations/models only when your copied-out project needs
  persistence; this starter intentionally ships with an in-memory example
  service.
- Keep `vendor/`, `node_modules/`, `.env`, and generated caches out of git.

## Common issues

- **`No application encryption key has been specified`** — run
  `php artisan key:generate` after copying `.env.example` to `.env`.
- **Composer is not installed locally** — use `docker run --rm -v "$PWD:/app" -w /app composer:2 composer install`.
- **API validation returns HTML** — send `Accept: application/json` or use
  `/api/*`; this starter forces JSON rendering for API paths.

# PHP Starters

Self-contained PHP basecode templates. Copy a starter folder out of this
repository and it runs as-is — no files outside the folder are referenced.

| Starter | Category | Description |
|---|---|---|
| [`vanilla`](./vanilla/) | library | Zero-dependency library/CLI base: composer PSR-4 autoload, fail-fast env config, leveled console logging, example service, dependency-free test runner |
| [`laravel`](./laravel/) | backend | Laravel 13 REST API base: `/up` health, JSON API errors, example resource, PHPUnit tests, Docker |

## Verification strategy

- `vanilla` is verified locally with the PHP CLI (test suite, CLI smoke run).
- `laravel` uses the official Laravel skeleton plus ForgeBase API layer;
  dependencies are lockfile-pinned and verified with Composer/Docker on PHP 8.4
  when the PHP ecosystem gate is run.
- The composer manifest is validated with the official `composer:2` image,
  and the test suite runs again on the `php:8.3-cli` image to prove the
  declared version floor where Docker is available.

## Copying a starter out

```bash
cp -r languages/php/vanilla /path/to/my-project
cd /path/to/my-project
# rename the "forgebase/starter" package and the ForgeBase\Starter namespace
composer install   # optional: with no dependencies, only the autoloader changes
php tests/run.php
```

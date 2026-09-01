# PHP Starters

Self-contained PHP basecode templates. Copy a starter folder out of this
repository and it runs as-is — no files outside the folder are referenced.

| Starter | Category | Description |
|---|---|---|
| [`vanilla`](./vanilla/) | library | Zero-dependency library/CLI base: composer PSR-4 autoload, fail-fast env config, leveled console logging, example service, dependency-free test runner |

## Verification strategy

- `vanilla` is verified locally with the PHP CLI (test suite, CLI smoke run).
- The composer manifest is validated with the official `composer:2` image,
  and the test suite runs again on the `php:8.3-cli` image to prove the
  declared version floor.

## Copying a starter out

```bash
cp -r languages/php/vanilla /path/to/my-project
cd /path/to/my-project
# rename the "forgebase/starter" package and the ForgeBase\Starter namespace
composer install   # optional: with no dependencies, only the autoloader changes
php tests/run.php
```

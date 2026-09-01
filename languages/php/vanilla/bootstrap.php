<?php

declare(strict_types=1);

/*
 * Autoload bootstrap. Composer's autoloader is authoritative when
 * vendor/ exists (after `composer install`); the PSR-4 fallback keeps the
 * zero-dependency workflow working before that first install.
 */

if (is_file(__DIR__ . '/vendor/autoload.php')) {
    require __DIR__ . '/vendor/autoload.php';
    return;
}

spl_autoload_register(static function (string $class): void {
    $prefix = 'ForgeBase\\Starter\\';
    if (!str_starts_with($class, $prefix)) {
        return;
    }

    $relative = substr($class, strlen($prefix));
    $file = __DIR__ . '/src/' . str_replace('\\', '/', $relative) . '.php';
    if (is_file($file)) {
        require $file;
    }
});

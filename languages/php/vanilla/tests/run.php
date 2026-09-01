<?php

declare(strict_types=1);

/*
 * Dependency-free test runner: discovers tests/*Test.php, instantiates each
 * class, and runs every public zero-argument method whose name starts with
 * "test". Exits non-zero when any expectation fails, so CI can gate on it.
 */

require __DIR__ . '/bootstrap.php';

$failures = [];
$passed = 0;
$files = glob(__DIR__ . '/*Test.php') ?: [];

foreach ($files as $file) {
    $class = 'StarterTests\\' . basename($file, '.php');
    require $file;

    $reflection = new ReflectionClass($class);
    $instance = $reflection->newInstance();

    foreach ($reflection->getMethods(ReflectionMethod::IS_PUBLIC) as $method) {
        $name = $method->getName();
        if (!str_starts_with($name, 'test') || $method->getNumberOfParameters() > 0) {
            continue;
        }

        try {
            $instance->{$name}();
            $passed++;
            echo "  PASS {$class}::{$name}\n";
        } catch (Throwable $thrown) {
            $failures[] = "{$class}::{$name}: {$thrown->getMessage()}";
            echo "  FAIL {$class}::{$name}\n";
        }
    }
}

echo "\n";
if ($failures !== []) {
    echo 'FAILURES (' . count($failures) . "):\n";
    foreach ($failures as $failure) {
        echo "  - {$failure}\n";
    }
    exit(1);
}

echo "OK ({$passed} tests)\n";

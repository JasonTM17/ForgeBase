<?php

declare(strict_types=1);

/*
 * Micro test-support helpers for the dependency-free runner. Throw on the
 * first failed expectation; run.php records the result per test method.
 * Swap the runner for PHPUnit once the copied-out project adds dev
 * dependencies.
 */

function expect_true(bool $condition, string $message): void
{
    if (!$condition) {
        throw new RuntimeException("expectation failed: {$message}");
    }
}

function expect_same(mixed $expected, mixed $actual, string $message = ''): void
{
    if ($expected !== $actual) {
        $detail = $message === '' ? '' : " ({$message})";
        throw new RuntimeException(sprintf(
            'expectation failed: expected %s, got %s%s',
            var_export($expected, true),
            var_export($actual, true),
            $detail
        ));
    }
}

function expect_throws(string $exceptionClass, callable $fn, string $message = ''): void
{
    try {
        $fn();
    } catch (Throwable $thrown) {
        expect_true(
            $thrown instanceof $exceptionClass,
            sprintf(
                '%sexpected %s, got %s: %s',
                $message === '' ? '' : "{$message}: ",
                $exceptionClass,
                get_class($thrown),
                $thrown->getMessage()
            )
        );

        return;
    }

    throw new RuntimeException(sprintf(
        'expectation failed: expected %s to be thrown, nothing was%s',
        $exceptionClass,
        $message === '' ? '' : " ({$message})"
    ));
}

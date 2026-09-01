<?php

declare(strict_types=1);

namespace StarterTests;

use ForgeBase\Starter\Greeter;

final class GreeterTest
{
    public function testGreetsByName(): void
    {
        expect_same('Hello, ForgeBase!', (new Greeter())->greet('ForgeBase'));
    }

    public function testRejectsEmptyNames(): void
    {
        $greeter = new Greeter();
        expect_throws(
            \InvalidArgumentException::class,
            static fn () => $greeter->greet('   ')
        );
    }
}

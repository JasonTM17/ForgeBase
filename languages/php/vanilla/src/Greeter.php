<?php

declare(strict_types=1);

namespace ForgeBase\Starter;

/**
 * Example domain service. It exists to demonstrate the shape a real service
 * takes (validation -> behavior), not to carry business meaning — replace
 * it when copying the template out.
 */
final class Greeter
{
    public function greet(string $name): string
    {
        if (trim($name) === '') {
            throw new \InvalidArgumentException('name must not be empty');
        }

        return "Hello, {$name}!";
    }
}

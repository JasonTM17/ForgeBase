<?php

namespace App\Services;

use InvalidArgumentException;

class ExampleService
{
    /** @var array<int, array{id: int, name: string}> */
    private array $items = [];

    private int $nextId = 1;

    /** @return array{id: int, name: string} */
    public function create(string $name): array
    {
        $name = trim($name);

        if ($name === '') {
            throw new InvalidArgumentException('name must not be empty');
        }

        $item = ['id' => $this->nextId++, 'name' => $name];
        $this->items[$item['id']] = $item;

        return $item;
    }

    /** @return array<int, array{id: int, name: string}> */
    public function list(): array
    {
        return array_values($this->items);
    }
}

<?php

namespace Tests\Unit;

use App\Services\ExampleService;
use InvalidArgumentException;
use PHPUnit\Framework\TestCase;

class ExampleServiceTest extends TestCase
{
    public function test_it_creates_examples(): void
    {
        $service = new ExampleService;

        $this->assertSame(['id' => 1, 'name' => 'first'], $service->create(' first '));
        $this->assertCount(1, $service->list());
    }

    public function test_it_rejects_blank_names(): void
    {
        $this->expectException(InvalidArgumentException::class);
        $this->expectExceptionMessage('name must not be empty');

        (new ExampleService)->create('   ');
    }
}

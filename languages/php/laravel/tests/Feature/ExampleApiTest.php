<?php

namespace Tests\Feature;

use Tests\TestCase;

class ExampleApiTest extends TestCase
{
    public function test_root_returns_envelope(): void
    {
        $this->getJson('/')
            ->assertOk()
            ->assertJsonPath('message', 'ok')
            ->assertJsonPath('data.service', 'ForgeBase Laravel');
    }

    public function test_health_endpoint_is_available(): void
    {
        $this->get('/up')->assertOk();
    }

    public function test_example_endpoint_lists_items(): void
    {
        $this->getJson('/api/examples')
            ->assertOk()
            ->assertJsonPath('message', 'ok')
            ->assertJsonPath('data', []);
    }

    public function test_example_endpoint_validates_input_without_stack_traces(): void
    {
        $this->postJson('/api/examples', ['name' => ''])
            ->assertUnprocessable()
            ->assertJsonMissingPath('exception')
            ->assertJsonMissingPath('trace');
    }
}

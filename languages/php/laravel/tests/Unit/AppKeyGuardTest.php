<?php

namespace Tests\Unit;

use App\Providers\AppServiceProvider;
use RuntimeException;
use Tests\TestCase;

class AppKeyGuardTest extends TestCase
{
    public function test_boot_aborts_without_key_outside_local_and_testing(): void
    {
        config(['app.key' => null]);
        $this->app->detectEnvironment(fn () => 'production');

        $this->expectException(RuntimeException::class);
        $this->expectExceptionMessage('APP_KEY is required');

        (new AppServiceProvider($this->app))->boot();
    }

    public function test_boot_allows_local_without_key(): void
    {
        config(['app.key' => null]);
        $this->app->detectEnvironment(fn () => 'local');

        (new AppServiceProvider($this->app))->boot();

        $this->assertTrue(true);
    }

    public function test_boot_allows_production_with_key(): void
    {
        config(['app.key' => 'base64:dGVzdC1rZXk=']);
        $this->app->detectEnvironment(fn () => 'production');

        (new AppServiceProvider($this->app))->boot();

        $this->assertTrue(true);
    }
}

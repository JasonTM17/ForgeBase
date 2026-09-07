<?php

namespace Tests\Unit;

use App\Providers\AppServiceProvider;
use RuntimeException;
use Tests\TestCase;

class AppKeyGuardTest extends TestCase
{
    public function test_boot_aborts_without_key_outside_local_and_testing(): void
    {
        $this->withArtisanCommand('queue:work', function (): void {
            config(['app.key' => null]);
            $this->app->detectEnvironment(fn () => 'production');

            $this->expectException(RuntimeException::class);
            $this->expectExceptionMessage('APP_KEY is required');

            (new AppServiceProvider($this->app))->boot();
        });
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

    public function test_boot_allows_artisan_test_before_phpunit_environment_loads(): void
    {
        $this->withArtisanCommand('test', function (): void {
            config(['app.key' => null]);
            $this->app->detectEnvironment(fn () => 'production');

            (new AppServiceProvider($this->app))->boot();
        });

        $this->assertTrue(true);
    }

    public function test_boot_allows_key_generation_without_existing_key(): void
    {
        $this->withArtisanCommand('key:generate', function (): void {
            config(['app.key' => null]);
            $this->app->detectEnvironment(fn () => 'production');

            (new AppServiceProvider($this->app))->boot();
        });

        $this->assertTrue(true);
    }

    /**
     * @param callable(): void $callback
     */
    private function withArtisanCommand(string $command, callable $callback): void
    {
        $originalArgv = $_SERVER['argv'] ?? null;
        $_SERVER['argv'] = ['artisan', $command];

        try {
            $callback();
        } finally {
            if ($originalArgv === null) {
                unset($_SERVER['argv']);
            } else {
                $_SERVER['argv'] = $originalArgv;
            }
        }
    }
}

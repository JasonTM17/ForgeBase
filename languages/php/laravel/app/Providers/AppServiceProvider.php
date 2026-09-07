<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use RuntimeException;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        if (
            empty(config('app.key'))
            && ! $this->app->environment(['local', 'testing'])
            && ! $this->allowsMissingKeyForConsoleCommand()
        ) {
            throw new RuntimeException(
                'APP_KEY is required outside local and testing environments. '
                .'Copy .env.example to .env, then run: php artisan key:generate'
            );
        }
    }

    private function allowsMissingKeyForConsoleCommand(): bool
    {
        if (! $this->app->runningInConsole()) {
            return false;
        }

        return in_array($_SERVER['argv'][1] ?? '', ['key:generate', 'test'], true);
    }
}

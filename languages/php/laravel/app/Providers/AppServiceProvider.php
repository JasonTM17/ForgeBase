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
        if (empty(config('app.key')) && ! $this->app->environment(['local', 'testing'])) {
            throw new RuntimeException(
                'APP_KEY is required outside local and testing environments. '
                .'Copy .env.example to .env, then run: php artisan key:generate'
            );
        }
    }
}

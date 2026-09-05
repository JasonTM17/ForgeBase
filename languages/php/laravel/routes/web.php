<?php

use Illuminate\Support\Facades\Route;

Route::get('/', fn () => response()->json([
    'data' => ['service' => config('app.name')],
    'message' => 'ok',
]));

<?php

namespace App\Http\Controllers;

use App\Services\ExampleService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use InvalidArgumentException;

class ExampleController extends Controller
{
    public function __construct(private readonly ExampleService $examples) {}

    public function index(): JsonResponse
    {
        return response()->json([
            'data' => $this->examples->list(),
            'message' => 'ok',
        ]);
    }

    public function store(Request $request): JsonResponse
    {
        $payload = $request->validate([
            'name' => ['required', 'string', 'max:100'],
        ]);

        try {
            $item = $this->examples->create($payload['name']);
        } catch (InvalidArgumentException $exception) {
            return response()->json([
                'error' => [
                    'code' => 'INVALID_ARGUMENT',
                    'message' => $exception->getMessage(),
                ],
            ], 422);
        }

        return response()->json([
            'data' => $item,
            'message' => 'created',
        ], 201);
    }
}

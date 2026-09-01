<?php

declare(strict_types=1);

namespace ForgeBase\Starter;

/**
 * Fail-fast configuration: missing required variables or values that fail
 * validation abort startup before any real work happens, so
 * misconfiguration is never discovered in production traffic.
 */
final class EnvConfig
{
    private function __construct(
        public readonly string $serviceName,
        public readonly LogSeverity $logLevel,
    ) {
    }

    /** @param array<string, string|false> $environment */
    public static function fromEnvironment(array $environment = []): self
    {
        $environment = $environment === [] ? getenv() : $environment;

        $serviceName = self::required($environment, 'SERVICE_NAME');
        $logLevelValue = self::optional($environment, 'APP_LOG_LEVEL', 'information');
        $logLevel = LogSeverity::tryFrom(strtolower($logLevelValue))
            ?? throw new EnvConfigException(sprintf(
                "APP_LOG_LEVEL '%s' is invalid. Valid values: %s.",
                $logLevelValue,
                implode(', ', array_column(LogSeverity::cases(), 'value')),
            ));

        return new self($serviceName, $logLevel);
    }

    /** @param array<string, string|false> $environment */
    private static function required(array $environment, string $name): string
    {
        $value = $environment[$name] ?? '';
        if (!is_string($value) || trim($value) === '') {
            throw new EnvConfigException(
                "required environment variable {$name} is missing or empty"
            );
        }

        return $value;
    }

    /** @param array<string, string|false> $environment */
    private static function optional(
        array $environment,
        string $name,
        string $fallback
    ): string {
        $value = $environment[$name] ?? '';
        return is_string($value) && trim($value) !== '' ? $value : $fallback;
    }
}

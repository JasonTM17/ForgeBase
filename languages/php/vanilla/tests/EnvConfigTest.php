<?php

declare(strict_types=1);

namespace StarterTests;

use ForgeBase\Starter\EnvConfig;
use ForgeBase\Starter\EnvConfigException;
use ForgeBase\Starter\LogSeverity;

final class EnvConfigTest
{
    public function testThrowsWhenRequiredVariableIsMissing(): void
    {
        expect_throws(EnvConfigException::class, static fn () => EnvConfig::fromEnvironment([]));
    }

    public function testThrowsWhenRequiredVariableIsEmpty(): void
    {
        expect_throws(
            EnvConfigException::class,
            static fn () => EnvConfig::fromEnvironment(['SERVICE_NAME' => '   '])
        );
    }

    public function testDefaultsLogLevelToInformation(): void
    {
        $config = EnvConfig::fromEnvironment(['SERVICE_NAME' => 'demo']);

        expect_same(LogSeverity::Information, $config->logLevel);
    }

    public function testThrowsOnUnknownLogLevel(): void
    {
        expect_throws(
            EnvConfigException::class,
            static fn () => EnvConfig::fromEnvironment([
                'SERVICE_NAME' => 'demo',
                'APP_LOG_LEVEL' => 'loud',
            ])
        );
    }

    public function testParsesLogLevelCaseInsensitively(): void
    {
        $config = EnvConfig::fromEnvironment([
            'SERVICE_NAME' => 'demo',
            'APP_LOG_LEVEL' => 'Warning',
        ]);

        expect_same(LogSeverity::Warning, $config->logLevel);
    }
}

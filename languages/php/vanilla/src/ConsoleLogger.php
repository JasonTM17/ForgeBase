<?php

declare(strict_types=1);

namespace ForgeBase\Starter;

/**
 * Minimal leveled logger: ISO-8601 UTC timestamp, severity tag, and service
 * context on every line. Errors go to stderr so redirection keeps
 * diagnostics out of data pipelines. Replace with a structured logging
 * library when the copied-out project needs richer sinks.
 */
final class ConsoleLogger
{
    public function __construct(
        private readonly LogSeverity $threshold,
        private readonly string $service,
    ) {
    }

    public function info(string $message): void
    {
        $this->write(LogSeverity::Information, $message);
    }

    public function warning(string $message): void
    {
        $this->write(LogSeverity::Warning, $message);
    }

    public function error(string $message): void
    {
        $this->write(LogSeverity::Error, $message);
    }

    private function write(LogSeverity $severity, string $message): void
    {
        if ($severity->rank() > $this->threshold->rank()) {
            return;
        }

        $line = sprintf(
            "%s [%s] service=%s %s\n",
            gmdate('Y-m-d\TH:i:s.v\Z'),
            $severity->tag(),
            $this->service,
            $message
        );

        if ($severity->isError()) {
            fwrite(STDERR, $line);

            return;
        }

        fwrite(STDOUT, $line);
    }
}

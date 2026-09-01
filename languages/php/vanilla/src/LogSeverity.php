<?php

declare(strict_types=1);

namespace ForgeBase\Starter;

/**
 * Severity levels for the built-in console logger, ordered from most to
 * least severe. A local enum keeps the starter dependency-free; swap for a
 * logging library when the copied-out project grows.
 */
enum LogSeverity: string
{
    case Critical = 'critical';
    case Error = 'error';
    case Warning = 'warning';
    case Information = 'information';
    case Debug = 'debug';
    case Trace = 'trace';

    /** Short uppercase tag used in log lines, e.g. "INF". */
    public function tag(): string
    {
        return strtoupper(substr($this->name, 0, 3));
    }

    /** Integer rank (lower = more severe); string-backed enums must not be
     * compared directly because alphabetical order is not severity order. */
    public function rank(): int
    {
        return match ($this) {
            self::Critical => 0,
            self::Error => 1,
            self::Warning => 2,
            self::Information => 3,
            self::Debug => 4,
            self::Trace => 5,
        };
    }

    /** Errors and worse belong on stderr. */
    public function isError(): bool
    {
        return $this === self::Error || $this === self::Critical;
    }
}

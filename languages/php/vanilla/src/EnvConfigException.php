<?php

declare(strict_types=1);

namespace ForgeBase\Starter;

/** Raised only for configuration problems, so hosts can catch it and exit
 * with a clean message instead of a stack trace. */
final class EnvConfigException extends \RuntimeException
{
}

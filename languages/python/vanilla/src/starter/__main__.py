"""CLI entry point: ``python -m starter`` or the ``starter`` console script."""

from __future__ import annotations

import argparse
import logging
import sys

from starter import AppConfig, ConfigError, GreeterService, configure_logging

logger = logging.getLogger(__name__)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="starter", description="ForgeBase vanilla Python starter")
    parser.add_argument("name", help="name to greet")
    args = parser.parse_args(argv)

    try:
        config = AppConfig.from_env()
    except ConfigError as exc:
        # Config problems are fatal and must not print a traceback to users.
        print(f"configuration error: {exc}", file=sys.stderr)
        return 1
    configure_logging(config)
    logger.info("application started")

    greeter = GreeterService()
    print(greeter.greet(args.name))
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""starter — ForgeBase vanilla Python starter package.

A stdlib-only base for Python libraries and CLIs: environment-driven
configuration, structured JSON logging, and an example service.
"""

from starter.config import AppConfig, ConfigError
from starter.greeter import GreeterService
from starter.logging_setup import configure_logging

__all__ = ["AppConfig", "ConfigError", "GreeterService", "configure_logging"]

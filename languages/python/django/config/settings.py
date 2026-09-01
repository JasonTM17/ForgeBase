"""Django settings — environment-driven with fail-fast production checks.

This starter is API-only: admin/auth/session apps and the database are
intentionally absent (no ORM in Phase 1 — see docs/roadmap.md), so the
project boots without migrations. Add ``django.contrib`` apps and a
DATABASES block when your project needs them.
"""

from __future__ import annotations

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

VALID_ENVIRONMENTS = ("development", "testing", "production")
VALID_LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

APP_ENV = os.environ.get("FORGE_APP_ENV", "development")
if APP_ENV not in VALID_ENVIRONMENTS:
    raise ImproperlyConfigured(
        f"FORGE_APP_ENV must be one of {VALID_ENVIRONMENTS}, got {APP_ENV!r}"
    )
LOG_LEVEL = os.environ.get("FORGE_LOG_LEVEL", "INFO").upper()
if LOG_LEVEL not in VALID_LOG_LEVELS:
    raise ImproperlyConfigured(
        f"FORGE_LOG_LEVEL must be one of {VALID_LOG_LEVELS}, got {LOG_LEVEL!r}"
    )

# A missing secret key is a dev convenience and a production abort.
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
if APP_ENV == "production" and not SECRET_KEY:
    raise ImproperlyConfigured("DJANGO_SECRET_KEY is required in production")
SECRET_KEY = SECRET_KEY or "django-insecure-dev-only-key-change-me"

DEBUG = APP_ENV == "development"


def _env_list(name: str, default: list[str]) -> list[str]:
    raw = os.environ.get(name)
    if raw is None:
        return default
    return [item.strip() for item in raw.split(",") if item.strip()]


ALLOWED_HOSTS = _env_list("FORGE_ALLOWED_HOSTS", ["localhost", "127.0.0.1"])
if not DEBUG and not ALLOWED_HOSTS:
    raise ImproperlyConfigured("FORGE_ALLOWED_HOSTS is required in production")

INSTALLED_APPS = [
    # API-only starter: no admin/auth/contenttypes — nothing needs a database.
    "common.apps.CommonConfig",
    "examples.apps.ExamplesConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    # Maps domain/validation exceptions to the JSON error envelope.
    "common.middleware.ErrorEnvelopeMiddleware",
    # CsrfViewMiddleware is omitted: this is a stateless JSON API. If you add
    # cookie-based sessions or forms later, re-enable it.
]

ROOT_URLCONF = "config.urls"

TEMPLATES = []

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Security headers are safe defaults for an API; relax only with reason.
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"json": {"()": "config.json_logging.JsonFormatter"}},
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "json"},
    },
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
    "loggers": {
        "django": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "gunicorn.error": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
        "gunicorn.access": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": False},
    },
}

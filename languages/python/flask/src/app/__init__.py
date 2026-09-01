"""app — ForgeBase Flask starter application package.

Exposes the ``create_app`` application factory used by both ``flask run``
and ``gunicorn "app:create_app()"``.
"""

from __future__ import annotations

from flask import Flask

from app.core.config import load_config
from app.core.logging import configure_logging
from app.error_handlers import register_error_handlers
from app.examples import bp as examples_bp
from app.health import bp as health_bp


def create_app(config_overrides: dict | None = None) -> Flask:
    """Build and configure the Flask application.

    Kept as a factory so tests can build isolated instances and production
    runs via ``gunicorn "app:create_app()"``.
    """
    app = Flask(__name__)
    load_config(app)
    configure_logging(app)

    register_error_handlers(app)
    app.register_blueprint(health_bp)
    app.register_blueprint(examples_bp)

    if config_overrides:
        app.config.update(config_overrides)
    return app

"""Health blueprint: /health, /health/live, /health/ready."""

from __future__ import annotations

from flask import Blueprint, jsonify

bp = Blueprint("health", __name__)


@bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@bp.get("/health/live")
def liveness():
    # The process is running; no dependency checks here by definition.
    return jsonify({"status": "ok"})


@bp.get("/health/ready")
def readiness():
    # Add dependency probes (database, cache) here as the project grows.
    return jsonify({"status": "ok"})

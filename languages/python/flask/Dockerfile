# syntax=docker/dockerfile:1
# Multi-stage build: compile the dependency venv, copy it into a slim runtime.

FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app
COPY pyproject.toml uv.lock ./
# Dependencies only first, so source changes do not invalidate this layer.
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project --no-dev --no-editable

# README is needed because pyproject declares it as the wheel description.
COPY README.md ./
COPY src ./src
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev --no-editable


FROM python:3.12-slim-bookworm AS runtime

# Non-root runtime user; the app writes nothing to the filesystem.
RUN groupadd --system app && useradd --system --gid app app

WORKDIR /app
COPY --from=builder --chown=app:app /app/.venv /app/.venv
COPY --from=builder --chown=app:app /app/src /app/src

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

USER app
EXPOSE 8000

# Gunicorn is the production WSGI server; the factory keeps config env-driven.
CMD ["gunicorn", "app:create_app()", "--bind", "0.0.0.0:8000", "--workers", "2"]

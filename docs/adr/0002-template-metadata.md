# ADR 0002: Template metadata file

- Status: Accepted
- Date: 2026-09-01
- Context: ForgeBase repository foundation

## Context

The repository needs a machine-readable description of every template so that
tooling (validator, CI checks, future `forgebase create` CLI) can discover,
validate, and index templates without parsing READMEs or hard-coding paths.

## Decision

Every template carries a `forgebase.json` at its root with this schema:

```json
{
  "id": "python-fastapi",
  "name": "Python FastAPI Starter",
  "language": "python",
  "framework": "fastapi",
  "category": "backend",
  "tags": ["api", "rest"],
  "version": "1.0.0",
  "runtimeVersion": ">=3.12",
  "description": "Production-oriented FastAPI starter with config validation, structured logging, centralized error handling, health endpoints, and Docker."
}
```

Field rules:

- `id` — REQUIRED, unique repository-wide, MUST equal `<language>-<framework>`
  and match the template's directory location.
- `name` — REQUIRED, human-readable display name.
- `language`, `framework` — REQUIRED, lowercase directory names.
- `category` — REQUIRED, one of `backend`, `frontend`, `library`, `cli`,
  `mobile`.
- `tags` — REQUIRED array of lowercase strings (may be empty).
- `version` — REQUIRED, SemVer of the template itself (starts at 1.0.0).
- `runtimeVersion` — REQUIRED, human-readable runtime constraint string.
- `description` — REQUIRED, one or two sentences.

Validation is enforced by `scripts/validate_templates.py` and CI
(`repository-check.yml`). Unknown extra fields are rejected to keep the schema
honest.

## Alternatives considered

1. **No metadata; derive everything from paths** — works for id/language but
   cannot carry display name, category, tags, or description without parsing
   prose.
2. **One central registry file** — a single `templates.json` creates a
   cross-template coupling point and merge conflicts; per-template metadata
   keeps each template self-contained (ADR 0001 rule).
3. **Extra fields (author, license per template, variants)** — deferred until
   a consumer exists (YAGNI); the schema validator rejects unknown fields so
   adding them later is a conscious, reviewable change.

## Consequences

- Template discovery is a two-line directory scan.
- The future CLI needs no repository refactor.
- Metadata correctness is a CI gate, not a convention.

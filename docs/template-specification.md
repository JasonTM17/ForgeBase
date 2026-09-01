# ForgeBase Template Specification

This specification defines what every ForgeBase template MUST, SHOULD, and
OPTIONAL provide. It is intentionally capability-based, not layout-based:
templates stay idiomatic to their ecosystem (see
[architecture.md](architecture.md)) while guaranteeing a consistent baseline.

The normative keywords MUST / SHOULD / OPTIONAL follow RFC 2119.

Enforcement: `scripts/validate_templates.py` checks the file-level and
metadata requirements; CI runs it on every change (`.github/workflows/repository-check.yml`).

## 1. All templates (any category)

### MUST

- `README.md` — full documentation (see §5).
- `forgebase.json` — metadata per [ADR 0002](adr/0002-template-metadata.md);
  validated for schema, `id` uniqueness, and path consistency.
- `.gitignore` — appropriate to the ecosystem; no generated artifacts or
  secrets are ever committed.
- A working entrypoint — the template runs/builds as documented.
- At least one meaningful test — a test that would fail if core behavior
  (config loading, service logic, bootstrap) broke. No vanity tests.
- **Self-containment** — the template MUST NOT contain imports, includes,
  symlinks, or file references that escape its own directory. Concretely:
  no symlink anywhere inside the template; no absolute or host-specific
  paths (`/Users/...`, `/home/...`, `C:\...`); no references to repository
  tooling or other templates (`scripts/`, `.github/`, another
  `languages/...` path); no `../../../`-level traversal out of the template
  root; no workspace configs rooted outside the template (`go.work`, npm
  `workspaces`, cargo workspaces). Documentation links to repository-level
  docs are permitted — this is a static scan of tracked files, enforced by
  the validator with a negative fixture.

### SHOULD

- A linting and/or formatting toolchain with runnable commands documented in
  the README.
- Comments on non-obvious decisions (design rationale, security
  considerations), in English. No narrating comments.

### OPTIONAL

- Anything the ecosystem genuinely does not need (e.g., a Dockerfile for a
  plain library).

## 2. Backend API starters (`category: backend`)

Backend templates are network services. In addition to §1:

### MUST

- `.env.example` (or the framework-idiomatic equivalent, e.g. a documented
  `application.yml` env-override table) listing every supported environment
  variable, with safe empty/default values — never real credentials.
- Configuration system that reads environment variables and **fails fast at
  startup** on missing/invalid values.
- Structured or leveled logging with timestamps, level, and context — never
  bare `print`/`console.log` scattered through production code.
- Centralized error handling: one place maps internal errors to HTTP
  responses. Production responses MUST NOT leak stack traces, database
  errors, internal paths, or secrets. The error contract follows the
  framework's convention (see §4).
- Health endpoint(s) following the ecosystem's convention:
  - generic starters: `GET /health` returning `{"status": "ok"}` (or the
    ecosystem's idiomatic shape), plus liveness/readiness variants
    (`/health/live`, `/health/ready`) where the ecosystem does not define
    its own;
  - Spring Boot: actuator liveness/readiness probes;
  - Quarkus: `/q/health`, `/q/health/live`, `/q/health/ready`;
  - Ruby on Rails: `GET /up`.
- `Dockerfile` — multi-stage where beneficial, lightweight base image,
  non-root user, production-safe defaults, sane layer caching.
- `.dockerignore`.
- Tests covering: application bootstrap, the health endpoint(s), and one
  example use case.

### SHOULD

- Graceful shutdown on `SIGTERM`/`SIGINT` where the ecosystem supports it.
- An example resource endpoint demonstrating the request → validation →
  service → response flow (generic domain only — see §4).

### OPTIONAL

- `docker-compose.yml` — only when the template has external runtime
  dependencies (PostgreSQL, Redis, ...). Phase-1 templates have none.
- Database layer / ORM — deliberately excluded from Phase 1; see roadmap.

## 3. Frontend starters (`category: frontend` / `mobile`)

In addition to §1:

### MUST

- Typed environment-variable handling: public/runtime variables are declared
  in one typed config module, validated at startup (fail fast on missing
  values), and documented in `.env.example` or the framework-idiomatic
  equivalent (`runtimeConfig` for Nuxt, `$env` for SvelteKit).
- An error-handling surface: an error boundary component (SPA) or the
  framework's idiomatic error page/route (Next.js `error.tsx`, Nuxt
  `error.vue`, SvelteKit `+error.svelte`, Angular `ErrorHandler`, ...).
- At least one example component/page demonstrating the framework's idiomatic
  structure — generic domain only.
- Tests for the example component and config validation.
- `Dockerfile` (web-deployable frontend starters — SPA and SSR — only;
  mobile app starters such as `react-native` and `flutter` are exempt): SPA
  starters serve static output via nginx with SPA fallback, cache headers,
  and security headers; SSR starters run a non-root Node runtime.

### SHOULD

- Standardized npm scripts across all TypeScript templates: `lint`,
  `format:check`, `test`, `build` — so CI can drive every starter uniformly.
- Strict TypeScript configuration.

### OPTIONAL

- E2E testing (Playwright) — roadmap only for Phase 1.
- PWA, i18n, analytics scaffolding — out of scope.

## 4. Response and error contract

API templates keep an error contract consistent with their ecosystem:

- Frameworks without a dominant error standard (FastAPI, Express, Fastify,
  Gin, Fiber, stdlib Go, Flask) use a light envelope:
  - success: `{"data": ..., "message": "ok"}`
  - error: `{"error": {"code": "RESOURCE_NOT_FOUND", "message": "..."}}`
- Spring Boot uses RFC 9457 Problem Details (`spring-web` built-in).
- Quarkus follows the MicroProfile/RESTEasy conventions.
- Django, Laravel, Rails follow their framework's conventions for errors and
  health while keeping the MUST-level no-leak guarantees.

No template may ever expose stack traces, SQL errors, internal paths, secrets,
or implementation details in production responses.

## 5. README requirements (per template)

Every template README documents, in this order, adapted honestly to the
template:

1. Description (what it is, what stack)
2. Features
3. Requirements (runtime/tool versions)
4. Project structure (short tree)
5. Getting started / Installation (including "copy this folder out" + rename)
6. Configuration (every env variable, table or list)
7. Running (dev + production)
8. Testing
9. Linting / formatting
10. Docker
11. Production notes
12. Common issues

## 6. Metadata

`forgebase.json` schema, field rules, and validation behavior are defined in
[ADR 0002](adr/0002-template-metadata.md). The validator rejects unknown
fields, duplicate ids, id/path mismatches, and boundary violations
(self-containment MUST above); category values come from the ADR 0002 enum —
vanilla templates are categorized `library`.

## 7. Definition of done (per template)

A template is DONE when, for the environment where its toolchain is available:

- dependencies install;
- lint and format checks pass;
- tests pass;
- build passes;
- Docker build passes (if the template has a Dockerfile);
- README, `.env.example`/equivalent, and `forgebase.json` are accurate;
- no secrets, no generated artifacts, no placeholder code.

Where the local machine lacks the toolchain, the template documents its
Docker-based verification commands and CI status honestly (`NOT_RUN` until
observed).

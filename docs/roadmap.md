# ForgeBase Roadmap

This repository is a production-grade, multi-language / multi-framework
starter collection. Each `languages/<language>/<framework>/` folder is a
fully self-contained basecode a developer copies out to start a new
project.

## Current baseline: Phase 1 starter catalog

Phase 1 delivers 38 starters across 12 languages — backend APIs,
frontend SPAs/SSR, and mobile — with per-language path-filtered CI, a
template validator and complete open-source documentation. The current
repository also carries repo-local copy/create tooling and a generated public
verification matrix. Release claims remain tied to exact commits, tags, and
GitHub Actions evidence rather than this roadmap heading.

See the root [README](../README.md) for the full status table.

## Guiding principles

- **Self-contained first.** A template never reaches outside its own
  directory at runtime. Copy it out and it runs.
- **Idiomatic per ecosystem.** A FastAPI starter looks like FastAPI, a
  Spring Boot starter like Spring Boot. The repository defines a
  *capabilities* specification (config, logging, errors, health, tests,
  Docker), never a single mandatory file layout.
- **Verified over newest.** Templates pin the versions that were actually
  verified; anything unverifiable locally is labeled honestly as
  `NOT_RUN` with CI as the verification path.
- **Atomic Conventional Commits.** History is reviewable commit by commit.

## What is in scope (Phase 1)

- 38 starters: Python (vanilla, FastAPI, Flask, Django), TypeScript (node,
  express, NestJS, Fastify, React, Next.js, Vue, Nuxt, Angular, Svelte,
  SvelteKit, React Native), Java (vanilla, Spring Boot, Quarkus), Go
  (vanilla, Gin, stdlib net/http, Fiber), Rust (vanilla, Axum, Actix Web),
  C# (vanilla, ASP.NET Core), PHP (vanilla, Laravel), Ruby (vanilla, Rails),
  Kotlin (vanilla, Ktor), Dart (vanilla, Flutter), C (vanilla), C++
  (vanilla).
- Per-language path-filtered GitHub Actions CI.
- `scripts/validate_templates.py` enforcing the template specification.
- `scripts/check_copy_out.py` proving copied templates remain self-contained.
- `scripts/forgebase.py` for repo-local `list`, `show`, and `create`.
- `docs/verification-matrix.md` generated from template metadata.
- Open-source governance docs (CONTRIBUTING, SECURITY, CODE_OF_CONDUCT).

## What is explicitly out of scope (Phase 1)

- Packaged/global `forgebase` installation; the current CLI is repo-local.
- Database / ORM layers in starters (roadmap for production variants).
- `docker-compose.yml` (only earned when a template has external runtime
  dependencies; Phase 1 templates have none).
- E2E Playwright suites, PWA/i18n/analytics scaffolding.
- Mobile native builds (CI-first for Flutter / React Native).

## Roadmap (post-Phase 1)

| Priority | Item | Notes |
|---|---|---|
| P2 | Production template variants | `minimal` / `standard` / `production` under each framework |
| P2 | Database/ORM variants | PostgreSQL + a per-ecosystem ORM, composed on top of Phase-1 starters |
| P3 | Additional frameworks | Slim, Hono (where toolchains are available), Solid, Qwik, Astro |
| P3 | Additional languages | Elixir/Phoenix, Zig — when local toolchains exist to verify them |
| P3 | E2E testing harness | Playwright suites for the frontend starters |
| P3 | Template publishing | Versioned, per-template release artifacts |

## Deferred quality backlog

These items were deliberately kept out of Phase 1 or the current hardening
pass so the shipped starter contract remains bounded:

- Extract repeated GitHub Actions jobs with `workflow_call` after the current
  per-language workflows have run green on GitHub.
- Add `actionlint` once the repo chooses a maintained local/CI installation
  path for that tool.
- Add graceful shutdown wiring to the Kotlin Ktor starter when the Gradle
  gate can be re-run in its target toolchain.
- Review Go/Python whitespace and formatting drift as a dedicated style pass,
  not mixed into behavior fixes.
- Pin a concrete Dart/Flutter SDK version only after the repository has
  version evidence stronger than the current `stable` channel declaration.
- Decide whether the Quarkus starter should adopt a MicroProfile-style
  response envelope before changing its public response contract.

## How to contribute

- To add a **framework**: follow [docs/adding-a-framework.md](adding-a-framework.md).
- To add a **language**: follow [docs/adding-a-language.md](adding-a-language.md).
- Every new template MUST pass `scripts/validate_templates.py` and the
  focused gates for its ecosystem before review.

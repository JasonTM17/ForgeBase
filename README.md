# ForgeBase

**Production-grade starter templates for 12 languages and 38 starters.**

[![Repository checks](https://github.com/JasonTM17/ForgeBase/actions/workflows/repository-check.yml/badge.svg)](https://github.com/JasonTM17/ForgeBase/actions/workflows/repository-check.yml)
[![TypeScript](https://github.com/JasonTM17/ForgeBase/actions/workflows/typescript.yml/badge.svg)](https://github.com/JasonTM17/ForgeBase/actions/workflows/typescript.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Languages: English | [Tiếng Việt](README.vi.md)

ForgeBase is a curated catalog of self-contained boilerplate projects — one
folder per language and framework. Starting a new project means copying a
template instead of re-assembling structure, linting, testing, configuration,
logging, error handling, Docker, and CI from scratch.

| | |
| --- | --- |
| Catalog | 38 starters across 12 languages |
| Status | Phase 1 complete; per-starter evidence in the [verification matrix](docs/verification-matrix.md) |
| Governance | [MIT](LICENSE) · [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) |

## What is ForgeBase?

Every folder under `languages/<language>/<framework>/` is a complete,
independent project. Each one:

- **Runs on its own.** Copy it out of this repository and it works; templates
  never reach outside their own directory.
- **Follows its ecosystem.** FastAPI looks like FastAPI, Spring looks like
  Spring, Go looks like Go — never a forced one-size-fits-all architecture.
- **Has the critical boring pieces done properly.** Configuration management,
  structured logging, centralized error handling, health endpoints for APIs,
  tests, linting and formatting, Docker packaging, and documentation.

## Why ForgeBase?

- **Start in minutes, not hours** — production-oriented defaults from the
  first command.
- **Self-contained templates** — no hidden coupling; the repository around
  them is only documentation, tooling, and CI.
- **Honest engineering** — templates pin versions that were actually verified,
  and public claims use explicit evidence labels. Nothing is claimed to work
  that has not been run.

## Quick start

```bash
git clone https://github.com/JasonTM17/ForgeBase.git
cd ForgeBase

# list the catalog, inspect a starter, and copy it into a new project
python scripts/forgebase.py list
python scripts/forgebase.py show python-fastapi
python scripts/forgebase.py create python-fastapi ~/projects/my-api
cd ~/projects/my-api

# from here, follow the copied template's own README
```

Full copy-out guidance: [Using a ForgeBase Starter](docs/using-a-starter.md).

## Available starters

All 38 starters below are implemented and available (✅). Per-starter
verification evidence — local runs, official containers, and CI boundaries —
is recorded in the [verification matrix](docs/verification-matrix.md).

| Language | Starters (category) |
| --- | --- |
| Python ✅ | Vanilla (library/cli) · FastAPI (backend) · Flask (backend) · Django (backend) |
| TypeScript ✅ | Node (library/cli) · Express · NestJS · Fastify (backend) · React · Next.js · Vue · Nuxt · Angular · Svelte · SvelteKit (frontend) · React Native (mobile) |
| Java ✅ | Vanilla (library/cli) · Spring Boot (backend) · Quarkus (backend) |
| Go ✅ | Vanilla (library/cli) · net-http · Gin · Fiber (backend) |
| Rust ✅ | Vanilla (library/cli) · Axum (backend) · Actix Web (backend) |
| C# ✅ | Vanilla (library/cli) · ASP.NET Core (backend) |
| PHP ✅ | Vanilla (library/cli) · Laravel (backend) |
| Ruby ✅ | Vanilla (library/cli) · Rails (backend) |
| Kotlin ✅ | Vanilla (library/cli) · Ktor (backend) |
| Dart ✅ | Vanilla (library/cli) · Flutter (mobile) |
| C ✅ | Vanilla (library/cli) |
| C++ ✅ | Vanilla (library/cli) |

**Legend:** ✅ implemented and available · 🧪 implemented with local
verification `NOT_RUN` for the current host/toolchain · 🚧 planned or in
progress (see the [roadmap](docs/roadmap.md)).

Status reflects the latest recorded Phase 1 verification evidence: 38/38 ✅ in
the availability table, with affected starters re-run where host tooling or
official containers were available. For example, Kotlin Ktor's gates ran
inside the official `gradle:8.14-jdk21` container (`gradle test`, the
multi-stage image build, and a boot smoke check). Tagged releases and the
current `main` branch are separate evidence boundaries; PRs and release notes
must cite exact commits and tags.

## Quality and verification

ForgeBase changes follow a structured
[development workflow](docs/development-workflow.md): scout, plan, implement,
test, review, then release. Public claims use four evidence labels —
`PASS`, `FAIL`, `NOT_RUN`, and `BLOCKED` — and a local pass is never presented
as proof of CI, device behavior, or a published release.

Before any release claim, maintainers verify the template validator and its
selftest, workflow YAML parsing, Markdown link checks
(`scripts/check_docs_links.py`), repository boundary rules, secret patterns,
`git diff --check`, GitHub Actions on the exact pushed commit, and the release
tag. Dependabot triage, branch hygiene, branch protection, and release
evidence operations are documented in the
[maintainer guide](docs/maintainer-guide.md).

## Documentation map

The [documentation hub](docs/README.md) routes every reader — evaluator,
template author, maintainer — to the right page. Core references:

| Document | Purpose |
| --- | --- |
| [Using a ForgeBase Starter](docs/using-a-starter.md) | Select, copy out, rename, and verify a template |
| [Template specification](docs/template-specification.md) | The MUST/SHOULD baseline every starter provides |
| [Architecture](docs/architecture.md) | Repository layout, design decisions, boundaries |
| [Verification matrix](docs/verification-matrix.md) | Generated evidence index for starter status |
| [Conventions](docs/conventions.md) | Naming, commits, versioning, git workflow |
| [Development workflow](docs/development-workflow.md) | Evidence-based change and release process |
| [Maintainer guide](docs/maintainer-guide.md) | Day-to-day repository operations |
| [Roadmap](docs/roadmap.md) | Planned work and explicit non-goals |
| [Changelog](CHANGELOG.md) | Human release history, separate from evidence |

To add a starter, see [Adding a framework](docs/adding-a-framework.md) or
[Adding a language](docs/adding-a-language.md).

## Repository layout

```text
ForgeBase/
├── languages/        # one self-contained starter per <language>/<framework>
├── docs/             # architecture, template spec, conventions, guides, roadmap
│   ├── README.md     # documentation hub
│   └── adr/          # architectural decision records
├── scripts/          # repository tooling (validator, matrix, copy/create CLI)
└── .github/          # path-filtered CI workflows per language
```

## Development philosophy

Simplicity · Correctness · Maintainability · Developer experience ·
Security · Observability · Performance · Scalability

How these are applied: [architecture](docs/architecture.md) and
[template specification](docs/template-specification.md).

## Contributing, support, and security

Contributions of all sizes are welcome — start with
[CONTRIBUTING.md](CONTRIBUTING.md). Questions and reports are routed by
[SUPPORT.md](SUPPORT.md); suspected vulnerabilities follow
[SECURITY.md](SECURITY.md) through private reporting. This project follows the
[Code of Conduct](CODE_OF_CONDUCT.md) and is licensed under
[MIT](LICENSE).

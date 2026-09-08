# ForgeBase

**Production-grade starter templates for many languages and frameworks.**

[![Repository checks](https://github.com/JasonTM17/ForgeBase/actions/workflows/repository-check.yml/badge.svg)](https://github.com/JasonTM17/ForgeBase/actions/workflows/repository-check.yml)
[![TypeScript](https://github.com/JasonTM17/ForgeBase/actions/workflows/typescript.yml/badge.svg)](https://github.com/JasonTM17/ForgeBase/actions/workflows/typescript.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

Languages: English | [Tiếng Việt](README.vi.md)

ForgeBase is a curated collection of self-contained boilerplate projects —
one folder per language/framework — so that starting a new project means
copying a template instead of re-assembling structure, linting, testing,
configuration, logging, error handling, Docker, and CI from scratch.

> Status: Phase 1 complete — 38 starters across 12 languages, with the
> affected starters re-verified in the latest local pass where host tooling
> was available (Kotlin Ktor's gates ran in official toolchain containers).
> Rust/Ruby fixes were source-reviewed locally when those host toolchains were
> not available. Template availability and
> verification status are tracked in the
> [status table](#available-languages), with per-starter evidence in the
> [verification matrix](docs/verification-matrix.md); future work lives in the
> [roadmap](docs/roadmap.md).

> **Ghi chú tiếng Việt:** ForgeBase là bộ starter đa ngôn ngữ được kiểm chứng
> bằng CI, Docker, validator, và quy trình AK workflow công khai. Các file vận
> hành AgentKit cục bộ vẫn được giữ private và không publish lên GitHub.

## What is ForgeBase?

Every folder under `languages/<language>/<framework>/` is a complete,
independent project:

- runs on its own (copy it out of this repository and it works);
- follows the idiomatic conventions of its ecosystem — never a forced
  one-size-fits-all architecture;
- ships with the boring-but-critical pieces done properly: configuration
  management, logging, centralized error handling, health endpoints (APIs),
  tests, linting/formatting, Docker packaging, and documentation.

## Why ForgeBase?

- **Start in minutes, not hours** — production-oriented defaults from the
  first `git clone`.
- **Idiomatic, not uniform** — FastAPI looks like FastAPI, Spring looks like
  Spring, Go looks like Go.
- **Self-contained templates** — no hidden coupling between templates; the
  repository around them is only documentation, tooling, and CI.
- **Honest engineering** — templates pin versions that are actually verified;
  nothing is claimed to work that has not been run.

## Quality Gates

ForgeBase changes are maintained through an
[AgentKit-guided workflow](docs/agentkit-workflow.md): scout, plan, implement,
test, review, then release. Public claims use explicit evidence labels:
`PASS`, `FAIL`, `NOT_RUN`, and `BLOCKED`.

Before release, maintainers check the repository validator, its selftest,
workflow YAML parsing, docs links, generated-artifact boundaries, secret
patterns, `git diff --check`, exact-head GitHub Actions, and the release tag.
The public [verification matrix](docs/verification-matrix.md) records the
evidence label and CI boundary for each starter.
Maintainer operations such as Dependabot triage, branch hygiene, branch
protection, and release evidence are documented in the
[maintainer guide](docs/maintainer-guide.md).

## Documentation Map

Start with the [documentation hub](docs/README.md) if you are evaluating the
repository, contributing a new starter, or maintaining a release. Developers
copying a template should read [Using a ForgeBase Starter](docs/using-a-starter.md)
after choosing a starter id.

Core references:

- [verification matrix](docs/verification-matrix.md) — generated evidence
  index for starter status;
- [template specification](docs/template-specification.md) — required
  capabilities for every starter;
- [architecture](docs/architecture.md) — repository layout and boundaries;
- [roadmap](docs/roadmap.md) — planned work and explicit non-goals.

## Available Languages

| Language   | Starter      | Category     | Status |
| ---------- | ------------ | ------------ | ------ |
| Python     | Vanilla      | library/cli  | ✅ |
| Python     | FastAPI      | backend      | ✅ |
| Python     | Flask        | backend      | ✅ |
| Python     | Django       | backend      | ✅ |
| TypeScript | Node         | library/cli  | ✅ |
| TypeScript | Express      | backend      | ✅ |
| TypeScript | NestJS       | backend      | ✅ |
| TypeScript | Fastify      | backend      | ✅ |
| TypeScript | React        | frontend     | ✅ |
| TypeScript | Next.js      | frontend     | ✅ |
| TypeScript | Vue          | frontend     | ✅ |
| TypeScript | Nuxt         | frontend     | ✅ |
| TypeScript | Angular      | frontend     | ✅ |
| TypeScript | Svelte       | frontend     | ✅ |
| TypeScript | SvelteKit    | frontend     | ✅ |
| TypeScript | React Native | mobile       | ✅ |
| Java       | Vanilla      | library/cli  | ✅ |
| Java       | Spring Boot  | backend      | ✅ |
| Java       | Quarkus      | backend      | ✅ |
| Go         | Vanilla      | library/cli  | ✅ |
| Go         | net/http     | backend      | ✅ |
| Go         | Gin          | backend      | ✅ |
| Go         | Fiber        | backend      | ✅ |
| Rust       | Vanilla      | library/cli  | ✅ |
| Rust       | Axum         | backend      | ✅ |
| Rust       | Actix Web    | backend      | ✅ |
| C#         | Vanilla      | library/cli  | ✅ |
| C#         | ASP.NET Core | backend      | ✅ |
| PHP        | Vanilla      | library/cli  | ✅ |
| PHP        | Laravel      | backend      | ✅ |
| Ruby       | Vanilla      | library/cli  | ✅ |
| Ruby       | Rails        | backend      | ✅ |
| Kotlin     | Vanilla      | library/cli  | ✅ |
| Kotlin     | Ktor         | backend      | ✅ |
| Dart       | Vanilla      | library/cli  | ✅ |
| Dart       | Flutter      | mobile       | ✅ |
| C          | Vanilla      | library/cli  | ✅ |
| C++        | Vanilla      | library/cli  | ✅ |

**Legend:** ✅ = implemented and available · 🧪 = implemented with local
verification `NOT_RUN` for the current host/toolchain · 🚧 =
planned/in-progress (see the [roadmap](docs/roadmap.md)). Verification
evidence lives in the [verification matrix](docs/verification-matrix.md).

> Status reflects the latest recorded Phase 1 verification evidence:
> 38/38 ✅ in the availability table, with affected starters re-run where
> tooling or official containers were available. Tagged releases and the
> current `main` branch are separate evidence boundaries; use exact commit and
> tag evidence in PRs and release notes.
> Kotlin Ktor's gates ran inside the official `gradle:8.14-jdk21` container
> (no host Gradle toolchain): `gradle test`, the multi-stage image build, and
> a boot smoke check. A row flips to ✅ only after its focused gates pass on
> observed evidence.

## Quick Start

```bash
git clone https://github.com/JasonTM17/ForgeBase.git
cd ForgeBase

# pick a template and copy it to your new project
python scripts/forgebase.py list
python scripts/forgebase.py show python-fastapi
python scripts/forgebase.py create python-fastapi ~/projects/my-api
cd ~/projects/my-api

# follow the template's own README from here
```

More copy-out guidance: [docs/using-a-starter.md](docs/using-a-starter.md).

## Repository Structure

```text
ForgeBase/
├── languages/        # one self-contained starter per <language>/<framework>
│   ├── python/
│   ├── typescript/
│   ├── java/
│   ├── go/
│   ├── rust/
│   ├── csharp/
│   ├── php/
│   ├── ruby/
│   ├── kotlin/
│   ├── dart/
│   ├── c/
│   ├── cpp/
│   └── ...
├── docs/             # architecture, template spec, conventions, roadmap
│   ├── README.md
│   ├── using-a-starter.md
│   ├── verification-matrix.md
│   ├── template-specification.md
│   └── architecture.md
├── scripts/          # repository tooling (validation, matrix, copy/create)
└── .github/          # path-filtered CI workflows per language
```

## Development Philosophy

1. Simplicity 2. Correctness 3. Maintainability 4. Developer Experience
5. Security 6. Observability 7. Performance 8. Scalability

Details: [docs/architecture.md](docs/architecture.md) and
[docs/template-specification.md](docs/template-specification.md).

## Adding a New Template

See [docs/adding-a-language.md](docs/adding-a-language.md) and
[docs/adding-a-framework.md](docs/adding-a-framework.md).
For the release and review workflow, see
[docs/agentkit-workflow.md](docs/agentkit-workflow.md) and the
[maintainer guide](docs/maintainer-guide.md).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

See [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)

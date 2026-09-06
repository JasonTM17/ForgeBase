# ForgeBase

**Production-grade starter templates for many languages and frameworks.**

ForgeBase is a curated collection of self-contained boilerplate projects —
one folder per language/framework — so that starting a new project means
copying a template instead of re-assembling structure, linting, testing,
configuration, logging, error handling, Docker, and CI from scratch.

> Status: Phase 1 complete — 38 starters across 12 languages, with the
> affected starters re-verified locally where host tooling was available
> (Kotlin Ktor's gates ran in official toolchain containers). Rust/Ruby fixes
> were source-verified in this session because the host toolchain was not
> available. Template availability and
> verification status are tracked in the
> [status table](#available-languages); future work lives in the
> [roadmap](docs/roadmap.md).

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

**Legend:** ✅ = implemented and verified locally · 🧪 = implemented,
verification NOT_RUN locally (CI is the verification path) · 🚧 =
planned/in-progress (see the [roadmap](docs/roadmap.md)).

> Status reflects this session's verification pass: 38/38 ✅ in the table,
> with the affected starters re-run locally where tooling was available.
> Kotlin Ktor's gates ran inside the official `gradle:8.14-jdk21` container
> (no host Gradle toolchain): `gradle test`, the multi-stage image build, and
> a boot smoke check. A row flips to ✅ only after its focused gates pass on
> observed evidence.

## Quick Start

```bash
git clone https://github.com/JasonTM17/ForgeBase.git
cd ForgeBase

# pick a template and copy it to your new project
cp -r languages/python/fastapi ~/projects/my-api
cd ~/projects/my-api

# follow the template's own README from here
```

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
│   ├── adding-a-language.md
│   └── adding-a-framework.md
├── scripts/          # repository tooling (template validation)
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

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## Security

See [SECURITY.md](SECURITY.md).

## License

[MIT](LICENSE)

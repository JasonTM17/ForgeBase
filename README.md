# ForgeBase

**Production-grade starter templates for many languages and frameworks.**

ForgeBase is a curated collection of self-contained boilerplate projects —
one folder per language/framework — so that starting a new project means
copying a template instead of re-assembling structure, linting, testing,
configuration, logging, error handling, Docker, and CI from scratch.

> Status: under active construction. Template availability is tracked in the
> [status table](#available-languages) and the
> [roadmap](docs/roadmap.md) as templates land.

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

| Language   | Starter     | Category | Status |
| ---------- | ----------- | -------- | ------ |
| Python     | Vanilla     | library/cli | 🚧 planned |
| Python     | FastAPI     | backend  | 🚧 planned |
| Python     | Flask       | backend  | 🚧 planned |
| Python     | Django      | backend  | 🚧 planned |
| TypeScript | Node        | library/cli | 🚧 planned |
| TypeScript | Express     | backend  | 🚧 planned |
| TypeScript | NestJS      | backend  | 🚧 planned |
| TypeScript | Fastify     | backend  | 🚧 planned |
| TypeScript | React       | frontend | 🚧 planned |
| TypeScript | Next.js     | frontend | 🚧 planned |
| TypeScript | Vue         | frontend | 🚧 planned |
| TypeScript | Nuxt        | frontend | 🚧 planned |
| TypeScript | Angular     | frontend | 🚧 planned |
| TypeScript | Svelte      | frontend | 🚧 planned |
| TypeScript | SvelteKit   | frontend | 🚧 planned |
| TypeScript | React Native| mobile   | 🚧 planned |
| Java       | Vanilla     | library/cli | 🚧 planned |
| Java       | Spring Boot | backend  | 🚧 planned |
| Java       | Quarkus     | backend  | 🚧 planned |
| Go         | Vanilla     | library/cli | 🚧 planned |
| Go         | net/http    | backend  | 🚧 planned |
| Go         | Gin         | backend  | 🚧 planned |
| Go         | Fiber       | backend  | 🚧 planned |
| Rust       | Vanilla     | library/cli | 🚧 planned |
| Rust       | Axum        | backend  | 🚧 planned |
| Rust       | Actix Web   | backend  | 🚧 planned |
| C#         | Vanilla     | library/cli | 🚧 planned |
| C#         | ASP.NET Core| backend  | 🚧 planned |
| PHP        | Vanilla     | library/cli | 🚧 planned |
| PHP        | Laravel     | backend  | 🚧 planned |
| Ruby       | Vanilla     | library/cli | 🚧 planned |
| Ruby        | Rails      | backend  | 🚧 planned |
| Kotlin     | Vanilla     | library/cli | 🚧 planned |
| Kotlin     | Ktor        | backend  | 🚧 planned |
| Dart       | Vanilla     | library/cli | 🚧 planned |
| Dart       | Flutter     | mobile   | 🚧 planned |
| C          | Vanilla     | library/cli | 🚧 planned |
| C++        | Vanilla     | library/cli | 🚧 planned |

(✅ = implemented and verified locally; 🧪 = implemented, verification
NOT_RUN locally — CI is the verification path; 🚧 = planned, see the
[roadmap](docs/roadmap.md).)

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
│   └── ...
├── docs/             # architecture, template spec, conventions, roadmap
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

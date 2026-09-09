# Comprehensive Repository Documentation (Repo Doc)

Languages: English | [Tiếng Việt](repo-documentation.vi.md)

This document provides a comprehensive technical, architectural, and operational specification for the ForgeBase repository. Built upon the principles of Evidence-Driven Engineering and the structured AK Workflow, this document adheres strictly to professional standards without decorative icons or emojis, ensuring clarity, reproducibility, and enterprise readiness.

---

## 1. Project Overview and Design Philosophy

ForgeBase is a curated catalog of self-contained, production-grade starter templates covering **38 starters across 12 programming languages**.

### 1.1. Core Principles
- **Strictly Self-Contained:** Every template directory is a complete, standalone project. When copied out of ForgeBase, it runs immediately without relying on external scripts, parent directories, or shared workspace utilities.
- **Idiomatic per Ecosystem:** Codebases reflect the natural conventions of each language and framework (FastAPI conforms to Pythonic idioms, Spring Boot follows Enterprise Java standards, Go adheres to minimal idiomatic design). ForgeBase never imposes a single artificial directory structure across different ecosystems.
- **Production Foundations Built-In:** Every starter implements 6 non-negotiable architectural pillars: Configuration management, Structured logging, Centralized error handling, Health endpoints, Automated testing with linting, and Secure containerization (non-root Docker).
- **Generic Domain Only:** Starters feature a health check endpoint and at most one generic example resource (e.g., `items`). Specific business logic (such as Todo lists, Blogs, or E-commerce) is intentionally excluded to eliminate cleanup overhead when starting new projects.
- **Verification Honesty:** Public readiness claims must be grounded in recorded test evidence in the verification matrix. No starter is marked functional unless it has passed its verification checklist in the declared environment.

---

## 2. Repository Layout and Boundary Rules

### 2.1. Standard Directory Hierarchy

```text
ForgeBase/
├── languages/                  # Root directory for all starter templates
│   └── <language>/             # Language-specific directory
│       ├── README.md           # Language index summarizing its starters
│       └── <framework>/        # A self-contained, runnable starter project
│           ├── README.md       # Comprehensive template-level documentation
│           ├── forgebase.json  # Machine-readable metadata manifest
│           ├── Dockerfile      # Multi-stage production container build
│           ├── docker-compose.yml
│           └── ...             # Ecosystem-idiomatic project source code
├── docs/                       # Central repository documentation
│   ├── adr/                    # Architecture Decision Records
│   ├── architecture.md         # Repository architectural overview
│   ├── conventions.md          # Coding, style, and structure conventions
│   ├── template-specification.md # Mandatory baseline specification for starters
│   ├── verification-matrix.md  # Per-starter verification evidence matrix
│   ├── development-workflow.md # Engineering and verification workflow
│   ├── maintainer-guide.md     # Maintainer operational procedures
│   └── using-a-starter.md      # Copy-out and usage guide
├── scripts/                    # Automation tooling for testing and governance
│   ├── forgebase.py            # CLI management tool for catalog operations
│   ├── validate_templates.py   # Template structure and schema validator
│   ├── check_copy_out.py       # Isolated copy-out verification utility
│   ├── check_docs_links.py     # Markdown link and anchor slug validator
│   ├── update_verification_matrix.py # Evidence matrix synchronization script
│   └── test_forgebase_tools.py # Unit test suite for tooling scripts
├── .github/                    # CI/CD and governance automation
│   ├── workflows/              # Path-filtered CI workflows
│   ├── dependabot.yml          # Automated dependency maintenance schedule
│   └── PULL_REQUEST_TEMPLATE.md
├── CONTRIBUTING.md             # Contribution guidelines
├── SECURITY.md                 # Vulnerability reporting and security policy
├── CHANGELOG.md                # Release history and changelog
└── README.md                   # Repository overview
```

### 2.2. Boundary Rules

1. **Template and Repository Boundaries:**
   - Starter code must never reference files outside its own directory (no relative imports escaping via `../`, no dependencies on root configuration files).
   - Repository tools in `scripts/` and CI in `.github/` may inspect `languages/`, but templates must never invoke or depend on repository tooling.
   - Starters must not share runtime dependencies. Version parity across templates is deliberate duplication to guarantee copy-out isolation.

2. **Security and Secret Hygiene (Zero-Leak Policy):**
   - Developer environment files (`.vscode/`, `.idea/`) must not be committed.
   - Package dependency directories and virtual environments (`node_modules/`, `.venv/`, `vendor/`, `target/`) are strictly ignored.
   - Secrets, private keys, certificates, or actual environment files (`.env`, `*.pem`, `*.key`) are forbidden. All configurable variables must be documented in `.env.example`.
   - Agent execution transcripts, internal plan artifacts, and temporary caches must remain uncommitted.

---

## 3. Catalog Overview and Template Metadata

### 3.1. Catalog Breakdown (38 Starters / 12 Languages)

| Language | Directory | Category | Runtime / Framework Requirement |
| :--- | :--- | :--- | :--- |
| C | languages/c/vanilla | library | C11, Make |
| C++ | languages/cpp/vanilla | library | C++20, CMake |
| C# | languages/csharp/vanilla | library | .NET 8.0+, Console |
| C# | languages/csharp/aspnetcore | backend | .NET 8.0+, ASP.NET Core |
| Dart | languages/dart/vanilla | library | Dart 3.3+ |
| Dart | languages/dart/flutter | frontend / mobile | Flutter stable, Dart 3.3+ |
| Go | languages/go/vanilla | library | Go 1.25+ |
| Go | languages/go/net-http | backend | Go 1.25+, standard library |
| Go | languages/go/gin | backend | Go 1.25+, Gin framework |
| Go | languages/go/fiber | backend | Go 1.25+, Fiber framework |
| Java | languages/java/vanilla | library | OpenJDK 21, Maven |
| Java | languages/java/spring-boot | backend | OpenJDK 21, Spring Boot 3.4+, Maven |
| Java | languages/java/quarkus | backend | OpenJDK 21, Quarkus 3.17+, Maven |
| Kotlin | languages/kotlin/vanilla | library | OpenJDK 21, Gradle |
| Kotlin | languages/kotlin/ktor | backend | OpenJDK 21, Ktor 3.x, Gradle |
| PHP | languages/php/vanilla | library | PHP 8.3+, Composer |
| PHP | languages/php/laravel | backend | PHP 8.4+, Laravel 11.x, Composer |
| Python | languages/python/vanilla | library | Python 3.12+, Poetry / venv |
| Python | languages/python/fastapi | backend | Python 3.12+, FastAPI, Uvicorn |
| Python | languages/python/flask | backend | Python 3.12+, Flask |
| Python | languages/python/django | backend | Python 3.12+, Django |
| Ruby | languages/ruby/vanilla | library | Ruby 3.3+, Bundler |
| Ruby | languages/ruby/rails | backend | Ruby 3.3+, Rails 8.x |
| Rust | languages/rust/vanilla | library | Rust stable, Cargo |
| Rust | languages/rust/axum | backend | Rust stable, Axum 0.8 |
| Rust | languages/rust/actix-web | backend | Rust stable, Actix-web 4 |
| TypeScript | languages/typescript/node | library | Node.js 22+, npm |
| TypeScript | languages/typescript/express | backend | Node.js 22+, Express |
| TypeScript | languages/typescript/fastify | backend | Node.js 22+, Fastify |
| TypeScript | languages/typescript/nestjs | backend | Node.js 22+, NestJS |
| TypeScript | languages/typescript/react | frontend | Node.js 22+, Vite, React |
| TypeScript | languages/typescript/nextjs | frontend | Node.js 22+, Next.js App Router |
| TypeScript | languages/typescript/vue | frontend | Node.js 22+, Vite, Vue 3 |
| TypeScript | languages/typescript/nuxt | frontend | Node.js 22+, Nuxt 3 |
| TypeScript | languages/typescript/svelte | frontend | Node.js 22+, Vite, Svelte 5 |
| TypeScript | languages/typescript/sveltekit | frontend | Node.js 22+, SvelteKit |
| TypeScript | languages/typescript/angular | frontend | Node.js 22+, Angular CLI |
| TypeScript | languages/typescript/react-native | mobile | Expo SDK 52 / React Native |

### 3.2. Machine-Readable Metadata (`forgebase.json`)

Every template contains a top-level `forgebase.json` manifest enabling programmatic catalog discovery and auditing:

```json
{
  "$schema": "../../../docs/template-schema.json",
  "id": "python-fastapi",
  "language": "python",
  "framework": "fastapi",
  "category": "backend",
  "version": "1.0.0",
  "runtime": ">=3.12",
  "description": "Production-grade starter template for FastAPI with structured logging and Docker.",
  "ports": [8000],
  "entrypoint": "app/main.py",
  "commands": {
    "install": "pip install -r requirements.txt",
    "dev": "uvicorn app.main:app --reload",
    "test": "pytest",
    "lint": "ruff check .",
    "format": "ruff format --check ."
  }
}
```

---

## 4. Template Specification (The 6 Production Pillars)

As mandated by [template-specification.md](template-specification.md), every starter must fulfill six core requirements:

### 4.1. Configuration Management
- Configuration must be loaded from environment variables.
- Validation must be fail-fast at application boot: missing variables or invalid types must terminate the process immediately with descriptive diagnostics.
- A `.env.example` file must document all supported variables with safe local development defaults.

### 4.2. Structured Logging
- Backend starters must output structured JSON logs in production environments.
- Required fields include: timestamp (ISO 8601), log level (INFO, WARN, ERROR), message, and contextual metadata (e.g., request_id, trace_id).
- Raw print statements (`print()`, `console.log()`, `System.out.println`) are prohibited for application logging.

### 4.3. Centralized Error Handling
- Starters must implement global exception handling middleware or centralized filters.
- Error responses must follow a consistent JSON schema, preventing leak of stack traces or internal environment details in production.
- Conformance to RFC 7807 (Problem Details) is recommended.

### 4.4. Health Endpoints
- Backend services must expose `/health` or `/api/health`.
- The endpoint must return HTTP status `200 OK` when the service is healthy.
- Minimal payload format: `{"status": "pass"}` or `{"status": "ok"}`.

### 4.5. Testing, Linting, and Formatting
- Each template must include at least one unit test and one integration/smoke test verifying application initialization.
- Ecosystem-standard linter and formatter configurations must be present (e.g., `ruff` for Python, `eslint` for TypeScript, `golangci-lint` for Go).
- Test and lint commands must run locally without external infrastructure dependencies.

### 4.6. Container Packaging and Security
- Dockerfiles must implement multi-stage builds to optimize image footprint and build security.
- Containers must execute as non-root users by default.
- A functional `docker-compose.yml` must allow one-command local execution.

---

## 5. Repository Tooling Suite

Repository maintenance and verification are automated through scripts in `scripts/`:

### 5.1. `scripts/forgebase.py`
Catalog management CLI:
- `python scripts/forgebase.py list`: Display all 38 starters with categories and paths.
- `python scripts/forgebase.py show <id>`: Inspect starter metadata.
- `python scripts/forgebase.py create <id> <destination>`: Instantiate an isolated starter project.
- `python scripts/forgebase.py audit`: Perform code and structure audits across starters.

### 5.2. `scripts/validate_templates.py`
Core validation engine:
- Verifies required files: `README.md`, `forgebase.json`, `Dockerfile`, `docker-compose.yml`, dependency manifests.
- Validates `forgebase.json` schema and IDs.
- Detects directory escape violations.
- Self-test mode: `python scripts/validate_templates.py --selftest`.

### 5.3. `scripts/check_copy_out.py`
Copy-out isolation test:
- Copies templates to isolated temporary paths outside the repository.
- Validates that starters build and test without parent repository assets.

### 5.4. `scripts/check_docs_links.py`
Documentation integrity check:
- Validates all relative file links in tracked Markdown files.
- Verifies local Markdown anchor slugs against GitHub slug rules.

### 5.5. `scripts/update_verification_matrix.py`
Matrix synchronization:
- Syncs template metadata into [verification-matrix.md](verification-matrix.md).
- Verifies synchronization status with `--check`.

---

## 6. Engineering and Verification Workflow (AK Workflow)

Changes to ForgeBase follow a structured 6-phase evidence path:

```text
[1. Scout] -> [2. Plan] -> [3. Implement] -> [4. Test] -> [5. Review] -> [6. Release]
```

### 6.1. The Six Phases

| Phase | Focus | Exit Condition |
| :--- | :--- | :--- |
| **1. Scout** | Analyze codebase context, determine affected blast radius (templates, docs, scripts, workflows). | Affected boundaries and files are fully inventoried. |
| **2. Plan** | Formulate minimal viable changes, define outcome contracts, and specify expected verification commands. | Approved change plan and evidence targets documented. |
| **3. Implement** | Modify code or documentation strictly within approved scope. | Working tree diff matches planned scope without surplus edits. |
| **4. Test** | Run `validate_templates.py`, documentation checks, and ecosystem-specific gates. | All checks recorded with transparent evidence labels (`PASS`, `FAIL`, `NOT_RUN`, `BLOCKED`). |
| **5. Review** | Independent inspection of specification compliance, container security, secret avoidance, and portability. | All findings triaged and resolved. |
| **6. Release** | Merge to main following Release Gate clearance and remote CI validation. | Local commit matches `origin/main` with all remote checks passing on exact HEAD. |

### 6.2. Evidence Vocabulary

To prevent ambiguous readiness claims, ForgeBase mandates four explicit labels:

| Label | Technical Definition |
| :--- | :--- |
| `PASS` | The stated command, review, or external gate executed and succeeded on the designated scope. |
| `FAIL` | The check executed and uncovered a defect or specification deviation. |
| `NOT_RUN` | The check did not execute in the current environment; no pass is implied. |
| `BLOCKED` | The check could not proceed due to missing tools, credentials, infrastructure, or unapproved architectural decisions. |

---

## 7. Governance, Maintenance, and Release Gates

### 7.1. Branch Protection Policy
- The `main` branch is the production release branch.
- Mandatory protection settings:
  - Required CI status checks must pass before merging.
  - Pull requests require code review approval.
  - Force pushes (`git push --force`) and branch deletions are disabled.

### 7.2. Automated Dependency Maintenance (Dependabot)
- Monitored via `.github/dependabot.yml` across all 38 starters and GitHub Actions.
- Triage rules:
  1. Group updates by language ecosystem.
  2. Review dependency release notes for breaking changes.
  3. Validate locally with starter test suites.
  4. Fix any breakage with documented, cause-aligned updates; do not downgrade without cause.

### 7.3. Release Gate Checklist

Maintainers verify all items before tagging or publishing a release:

- [ ] `git status` is clean with no untracked files or leftover build artifacts.
- [ ] `python scripts/validate_templates.py --quiet` returns `PASS`.
- [ ] `python scripts/validate_templates.py --selftest` returns `PASS`.
- [ ] `python scripts/update_verification_matrix.py --check` returns `PASS`.
- [ ] `python scripts/check_docs_links.py --quiet` returns `PASS`.
- [ ] All `.github/workflows/*.yml` files parse successfully.
- [ ] No secrets, keys, or IDE artifacts are committed.
- [ ] `git diff --check` returns `PASS`.
- [ ] Local HEAD matches `origin/main`.
- [ ] GitHub Actions on exact release HEAD return `PASS`.

---

## 8. Starter Copy-Out Protocol

### 8.1. Initializing a New Project

**Option 1: Using the ForgeBase CLI (Recommended)**
```bash
# List available starters
python scripts/forgebase.py list

# Instantiate new project
python scripts/forgebase.py create python-fastapi ~/my-projects/order-service

# Navigate to project
cd ~/my-projects/order-service
```

**Option 2: Manual Copy**
```bash
cp -r languages/python/fastapi ~/my-projects/order-service
cd ~/my-projects/order-service
git init
```

### 8.2. Post-Copy Steps
1. Create local environment configuration:
   ```bash
   cp .env.example .env
   ```
2. Read the copied project's `README.md` for specific build and test instructions.
3. Verify container execution:
   ```bash
   docker compose up --build
   ```
4. Confirm health check at `http://localhost:<port>/health`.
5. Rename application references in package manifests (`package.json`, `pyproject.toml`, `go.mod`, `pom.xml`).

---

## 9. Navigation and Documentation Links

- [Documentation Hub](README.md)
- [Architecture Overview](architecture.md)
- [Template Baseline Specification](template-specification.md)
- [Conventions and Standards](conventions.md)
- [Development and Verification Workflow](development-workflow.md)
- [Maintainer Operations Guide](maintainer-guide.md)
- [Verification Matrix](verification-matrix.md)
- [Contribution Guidelines](../CONTRIBUTING.md)
- [Security Policy](../SECURITY.md)

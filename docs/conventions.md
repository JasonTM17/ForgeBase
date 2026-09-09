# ForgeBase Conventions

Repository-wide conventions that keep 38+ templates reviewable, comparable,
and CI-drivable. Template-internal code style is always the ecosystem's own
convention — this document governs the repository level. Related:
[development workflow](development-workflow.md) for the change process,
[architecture](architecture.md) for the layout rules these conventions assume.

## Naming

- Template directories: `languages/<language>/<framework>/`, lowercase,
  hyphenated when needed (`aspnetcore`, `net-http`, `react-native`).
- Template `id`: `<language>-<framework>` (e.g., `python-fastapi`).
- npm package names: `@forgebase/<framework>-starter`.
- Go module paths: `forgebase/go-<framework>` (local, non-published).
- Python package names: lowercase with underscores; `starter` (vanilla) and
  `app` (FastAPI) by convention.
- Java packages: `com.example.starter` — an explicit placeholder users rename.
- Branches: `feature/*`, `fix/*`, `docs/*`, `refactor/*`, `chore/*`.
- Tags, metadata fields, categories: lowercase.

## Folder conventions

- One template = one self-contained directory (ADR 0001). Templates never
  reach outside their folder at runtime.
- Language-level `README.md` indexes that language's starters and states the
  language's verification strategy (local toolchain vs Docker-based).
- Repository documentation lives in `docs/`; long-lived architectural
  decisions in `docs/adr/` (numbered, immutable once accepted — supersede via
  a new ADR).
- Repository tooling lives in `scripts/` and must stay dependency-light
  (standard library first) so CI runs it anywhere.

## Documentation conventions

- Every template README follows the section order in
  [template-specification.md §5](template-specification.md#5-readme-requirements-per-template).
- Commands in docs are copy-pasteable and portable (no personal paths, no
  hostnames).
- Status claims in docs match reality: verified features only; unimplemented
  ideas are `Planned` in the roadmap.
- Code comments: English; only for design decisions, workarounds, security
  considerations, and non-obvious behavior.

## Versioning

- ForgeBase itself: Semantic Versioning, starting at `0.1.0`.
  - MAJOR: breaking changes to the template specification, metadata schema,
    or repository layout.
  - MINOR: new templates, new docs, additive CI changes.
  - PATCH: fixes to existing templates/docs that do not change their
    contracts.
- Template `version` (in `forgebase.json`) tracks the template's own
  evolution, independently of the repository version.
- Framework/runtime versions inside templates are pinned to what was
  actually verified; bumps are ordinary MINOR/PATCH changes with re-verified
  evidence.

## Commit convention

Conventional Commits, one logical change per commit:

```text
<type>(<scope>): <imperative summary>

[optional body]
```

- Common types: `feat`, `fix`, `test`, `docs`, `build`, `ci`, `chore`,
  `refactor`, `perf`.
- Scopes: repository-wide changes use `(repo)`; template changes use the
  framework scope (`feat(fastapi)`, `feat(spring)`, `feat(gin)`,
  `feat(react)`, ...); language-wide changes use the language scope
  (`feat(python)`).
- A commit MUST NOT mix unrelated changes, MUST NOT commit generated
  artifacts (`node_modules/`, `__pycache__/`, `target/`, `dist/`, `build/`,
  `.env`, IDE/OS caches), and MUST leave `main` consistent.
- Before every commit: `git diff --check`, a secret scan of staged content,
  and the focused checks for the touched template.

## Git workflow

- `main` is always usable: every commit on it builds and passes its focused
  checks.
- Development happens on feature branches; `main` receives reviewed work.
- History is never rewritten on shared branches; no force push.

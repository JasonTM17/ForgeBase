# ForgeBase Architecture

This document explains how the ForgeBase repository is organized, why it is
organized that way, and the rules that keep it maintainable for years.

## Repository architecture

```text
ForgeBase/
├── languages/                  # ALL starter templates live here
│   └── <language>/             # one directory per language
│       ├── README.md           # language-level index of its starters
│       └── <framework>/        # ONE self-contained starter project
│           ├── README.md       # full per-template documentation
│           ├── forgebase.json  # template metadata (machine-readable)
│           └── ...             # ecosystem-idiomatic project files
├── docs/                       # repository documentation (not shipped with templates)
├── scripts/                    # repository tooling (template validator)
├── .github/workflows/          # path-filtered CI, one workflow per language
├── CONTRIBUTING.md, SECURITY.md, CODE_OF_CONDUCT.md, LICENSE
└── README.md
```

## Design decisions

### 1. Language-first hierarchy: `languages/<language>/<framework>/`

**Decision**: group templates by language first, framework second.

**Alternatives considered**:

- *Flat `templates/<language>-<framework>/`*: simpler globbing for a future
  CLI, but loses the language grouping humans navigate by, and the list gets
  harder to scan as it grows. The same flat index is trivially derived from
  `forgebase.json` metadata (see ADR 0002), so nothing is lost.
- *Category-first (`backend/`, `frontend/`, `mobile/`)*: categories overlap
  (a Next.js app can be both frontend and fullstack backend) and a framework
  would need to move directories if re-categorized. Language is a stable
  attribute; category is a judgement call kept in metadata.

**Consequences**: adding a framework = adding one directory; CI path filters
map 1:1 (`languages/python/**` → `python.yml`); a language's conventions can
be documented once at `languages/<language>/README.md`.

### 2. Templates are fully self-contained

Every `languages/<language>/<framework>/` directory is a complete project.
Copying it out of the repository must not break anything.

**Dependency rules**:

1. A template MUST NOT reference files outside its own directory at runtime
   (no shared libraries, no shared configuration, no relative imports that
   escape the folder). Documentation and repo-level CI are the only things
   that "know about" multiple templates.
2. Templates MUST NOT share runtime dependencies with each other. Two
   templates pinning the same library version is duplication, not coupling —
   that is intentional: templates evolve and are copied out independently.
3. Repository-level tooling (`scripts/`, `.github/`) may read templates
   (validation, CI) but templates must not read repository-level tooling.

**Consequence**: some boilerplate is repeated across templates. That is a
deliberate trade-off — the unit of reuse is the whole template, not code
inside it.

### 3. Idiomatic per ecosystem, not uniformly architected

Templates follow the conventions of their own ecosystem (FastAPI looks like
FastAPI, Spring Boot like Spring Boot, Go like Go). The repository defines a
*capabilities* specification — what a template MUST/SHOULD/OPTIONAL provide
(config, logging, errors, health, tests, Docker) — never a single mandatory
file layout. See `docs/template-specification.md`.

### 4. Generic domain only

Templates demonstrate architecture with a health endpoint and at most one
generic example resource. They must never grow into a specific application
(no todo/blog/ecommerce domains), because users copy them as a starting point,
not as a product to strip out.

### 5. Configuration and secrets

Templates read configuration from environment variables with fail-fast
validation at startup, and ship `.env.example` (or the framework-idiomatic
equivalent) documenting every variable. No secret ever exists in the
repository. Production-grade behavior (graceful shutdown, structured logging,
non-root containers) is built in rather than documented as a TODO.

### 6. Metadata as the machine-readable index

Each template carries `forgebase.json` (id, language, framework, category,
version, runtime version, description). This is the extension point for a
future `forgebase create` CLI: the CLI can discover templates by scanning
metadata instead of hard-coding paths, without any refactor of this layout.
See ADR 0002.

### 7. Verification honesty

Templates pin the versions that were actually verified. The repository's CI
runs each starter's ecosystem gates path-filtered; anything not verified
locally is labeled as such in the template's README. Unimplemented ideas live
in `docs/roadmap.md` as `Planned`, never as placeholder code.

## Boundaries summary

| Layer | May depend on | Must not depend on |
|---|---|---|
| Template (`languages/**`) | its own files, its pinned deps | other templates, repo tooling, host paths |
| Repo tooling (`scripts/`) | templates (read-only) | any single template's internals |
| CI (`.github/`) | paths, templates (build/test) | — |
| Docs | everything (read-only) | — |

## Evolution path

- **New framework**: add `languages/<language>/<framework>/` following
  `docs/adding-a-framework.md`. No existing file changes except the language
  index README and the status table.
- **New language**: add `languages/<language>/` following
  `docs/adding-a-language.md`, plus a CI workflow and roadmap entry.
- **Template variants** (`minimal`/`standard`/`production`): the layout does
  not block adding a variant level under a framework directory later; until
  then each template is a single "standard" variant and says so in metadata.
- **CLI (`forgebase create`)**: consumes `forgebase.json` metadata; the
  repository layout already treats templates as data.

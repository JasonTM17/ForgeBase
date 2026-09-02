# Adding a new language

This recipe adds a new language to ForgeBase. Follow it in order; every
step has an exit criterion.

## 1. Decide the verification strategy

Before writing code, decide how the new language's starters will be
verified:

- **Local toolchain available** (the SDK is installed in CI and, ideally,
  on the contributor's machine): verify locally and in CI.
- **Local toolchain absent**: verify inside an official Docker toolchain
  container in CI; mark local runs `NOT_RUN` honestly in the README.

Record the strategy in the language index README
(`languages/<language>/README.md`).

## 2. Create the language directory

```text
languages/<language>/
├── README.md           # language index + verification strategy
└── <framework>/        # one self-contained starter
```

The directory name MUST be lowercase; hyphenate multi-word names
(`react-native`, `aspnetcore`, `net-http`).

## 3. Write the language index README

`languages/<language>/README.md` MUST contain:

1. A table of that language's starters (framework, category, one-line
   description).
2. The verification strategy (local toolchain vs Docker-container).
3. A "copying a starter out" section.

Mirror the structure of an existing language README
(e.g. [languages/rust/README.md](../languages/rust/README.md)).

## 4. Scaffold each starter

For each framework:

1. Create `languages/<language>/<framework>/`.
2. Scaffold from the ecosystem's official generator where network allows
   (`cargo new`, `dotnet new`, `rails new`, `gradle init`, ...). Where it
   does not, write the idiomatic structure by hand and record the ruling.
3. Add the ForgeBase layer — see [docs/template-specification.md](template-specification.md):
   - fail-fast env config, structured logging, centralized error handling,
     health endpoints (for API starters), tests, README, `forgebase.json`,
     `.gitignore`, and (for API/SSR/SPA starters) a multi-stage non-root
     Dockerfile with `.dockerignore`.

## 5. Add `forgebase.json`

Every starter carries metadata per [ADR 0002](../adr/0002-template-metadata.md):

```json
{
  "id": "<language>-<framework>",
  "name": "<Language> <Framework> Starter",
  "language": "<language>",
  "framework": "<framework>",
  "category": "backend|frontend|library|cli|mobile",
  "tags": ["api", "rest"],
  "version": "1.0.0",
  "runtimeVersion": "<ecosystem version constraint>",
  "description": "One or two sentences."
}
```

`id` MUST equal `<language>-<framework>` and match the directory location.

## 6. Add a CI workflow

Add `.github/workflows/<language>.yml` (or extend an existing combined
workflow like `c-cpp.yml`). It MUST:

- Be **path-filtered** on `languages/<language>/**` so unrelated changes
  do not trigger it.
- Run the ecosystem's focused gates (lint, format, test; docker build for
  API/SSR/SPA starters).
- Use **caching** and **concurrency cancel-in-progress**.

Validate YAML locally:

```bash
python -c "import yaml, pathlib;
list(yaml.safe_load_all(pathlib.Path('.github/workflows/<language>.yml').read_text()))
print('OK')"
```

## 7. Verify and pass the gates

```bash
# Template spec compliance (runs against every starter)
python scripts/validate_templates.py

# The new starter's own gates (example: Rust)
cd languages/<language>/<framework>
cargo test && cargo fmt --check && cargo clippy -- -D warnings
```

The new starter MUST pass the validator and its focused gates before
review.

## 8. Update the root README status table

Add the new language's rows to the root [README](../README.md) status
table and update the totals.

## 9. Commit atomically

One logical change per Conventional Commit:

```text
feat(<language>): add <framework> starter
ci(repo): add <language> workflow
docs(repo): register <language> in root README + roadmap
```

## Exit criterion

- [ ] `languages/<language>/README.md` exists with the verification strategy
- [ ] Every starter passes `scripts/validate_templates.py`
- [ ] Every starter passes its ecosystem's focused gates
- [ ] `.github/workflows/<language>.yml` is path-filtered and valid YAML
- [ ] Root README status table updated

# Adding a new framework

This recipe adds a new framework under an existing language. It is
narrower than [adding a language](adding-a-language.md) — the language
index, CI workflow, and verification strategy already exist.

## 1. Confirm the framework fits the language

A framework MUST belong to the language whose ecosystem it is written in.
All TypeScript frameworks (backend and frontend) live under
`languages/typescript/`; all Python frameworks under `languages/python/`,
and so on. Category (backend / frontend / library / cli / mobile) is a
judgement call kept in `forgebase.json`, not in the directory layout.

## 2. Create the framework directory

```text
languages/<language>/<framework>/
```

Directory name rules: lowercase, hyphenate multi-word names
(`aspnetcore`, `net-http`, `react-native`).

## 3. Scaffold the starter

1. From the ecosystem's official generator where network allows
   (`create-vite`, `create-next-app`, `nuxi`, `ng new`, `sv create`,
   `django-admin`, `cargo new`, `dotnet new`, `rails new`, `gradle init`,
   ...). Where it does not, write the idiomatic structure by hand and
   record the ruling in the commit message.
2. Add the ForgeBase layer per
   [docs/template-specification.md](template-specification.md):
   - fail-fast env config, structured logging, centralized error handling,
   - health endpoints (API starters) or error boundary / typed env
     (frontend/mobile),
   - tests, README, `forgebase.json`, `.gitignore`,
   - multi-stage non-root Dockerfile + `.dockerignore` for API/SSR/SPA
     starters.

## 4. Add `forgebase.json`

Per [ADR 0002](../adr/0002-template-metadata.md). `id` MUST equal
`<language>-<framework>` and match the directory location.

## 5. Wire CI

Most languages have a matrix workflow keyed by `framework`. Add the new
framework to the `matrix.framework` list in
`.github/workflows/<language>.yml`. If the language has no workflow yet,
follow the language recipe instead.

## 6. Verify and pass the gates

```bash
python scripts/validate_templates.py     # spec compliance
cd languages/<language>/<framework>
# ... the ecosystem's focused gates (lint, format, test, docker build)
```

The new starter MUST pass the validator and its focused gates before
review.

## 7. Update the language index and root README

- Add the framework's row to `languages/<language>/README.md`.
- Add its row to the root [README](../README.md) status table and update
  totals.

## 8. Commit atomically

```text
feat(<framework>): add <language> <framework> starter
docs(repo): register <framework> in language index + root README
```

## Exit criterion

- [ ] Directory `languages/<language>/<framework>/` exists
- [ ] `forgebase.json` present with a matching `id`
- [ ] Passes `scripts/validate_templates.py`
- [ ] Passes the ecosystem's focused gates
- [ ] Listed in the language index README and root README status table

# ADR 0001: Template directory layout

- Status: Accepted
- Date: 2026-09-01
- Context: ForgeBase repository foundation

## Context

ForgeBase hosts many starter templates across many languages. The repository
needs a layout that (a) humans can navigate, (b) CI can path-filter, (c) a
future CLI can index, and (d) templates can be added to without restructuring
anything.

## Decision

Use `languages/<language>/<framework>/` as the canonical location of every
template. Language-level `README.md` files index the starters of a language.
Category (backend/frontend/library/cli/mobile) is recorded in each template's
`forgebase.json`, not encoded in the directory tree.

## Alternatives considered

1. **Flat `templates/<language>-<framework>/`** — simplest globbing; loses
   human-navigable grouping and per-language convention docs; flat index is
   derivable from metadata anyway.
2. **Category-first (`backend/`, `frontend/`, `mobile/`)** — categories overlap
   and change; a re-categorized template would move directories and break
   history/CI paths.

## Consequences

- Adding a framework is purely additive.
- CI path filters are 1:1 with language directories.
- Some boilerplate duplication across templates is accepted by design:
  templates are the unit of reuse.
- A future variant dimension (`minimal`/`standard`/`production`) can be added
  under a framework directory without breaking this layout.

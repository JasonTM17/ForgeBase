# Development and Verification Workflow

Languages: English | [Tiếng Việt](development-workflow.vi.md)

This document defines the engineering workflow ForgeBase uses to keep a large
starter catalog honest, reviewable, and reproducible. It governs template
creation, maintenance, and verification for everyone who changes the
repository. For repeatable day-to-day operations, pair this workflow with the
[maintainer guide](maintainer-guide.md).

## The Evidence Path

Every material change follows the same six-phase path:

| Phase | What happens | Exit condition |
| --- | --- | --- |
| 1. Scout | Identify the affected templates, docs, scripts, and CI workflows. | The full blast radius is listed. |
| 2. Plan | Define the smallest coherent change and the evidence it must produce. | Expected checks are written down. |
| 3. Implement | Change only the approved scope. | Diff matches the plan. |
| 4. Test | Run the validator plus the affected ecosystem gates. | Each check recorded with an evidence label. |
| 5. Review | Evaluate spec compliance, security, portability, and verification gaps. | Findings triaged (see below). |
| 6. Release | Publish only when repository state, commit, push, CI, and tag evidence all line up. | Release gate below passes. |

Small documentation-only changes may compress phases 2–5, but they still
require a clean diff, a link check, and no untracked or temporary files
staged.

Reviewer findings do not automatically expand scope. They become immediate
work only when they expose an in-scope defect, invalidate a release claim, or
block the current acceptance signal.

## Roles and Responsibilities

- **Author / implementer** scopes the change, performs the implementation,
  runs the local verification gates, and opens the pull request with honest
  evidence labels.
- **Reviewer** independently evaluates the proposed change for spec
  compliance, ecosystem idioms, security concerns, boundary constraints, and
  edge cases.
- **Maintainer** owns the final decision, checks GitHub Actions against the
  exact branch head, manages branch protection, merges changes, and tags
  releases.

## Evidence Vocabulary

ForgeBase uses four explicit evidence labels in README files, pull requests,
release notes, and the [verification matrix](verification-matrix.md):

| Label | Meaning |
| --- | --- |
| `PASS` | The stated command, review, or external check succeeded on the named scope. |
| `FAIL` | The check ran and found a defect. |
| `NOT_RUN` | The check did not run; no pass is implied. |
| `BLOCKED` | The check could not complete because a required tool, credential, service, permission, or decision was unavailable. |

These labels carry exactly these meanings. A local test pass does not prove
GitHub Actions, Docker publishing, device behavior, or production deployment;
treat each as a separate evidence boundary.

## Repository Boundaries

Contributors and maintainers keep local development noise and secrets out of
the published repository:

- Local editor and IDE settings (`.vscode/`, `.idea/`, and similar).
- Dependency trees and virtual environments (`node_modules/`, `.venv/`, `vendor/`).
- Build outputs, binaries, and caches (`dist/`, `build/`, `target/`, `.cache/`).
- Private secrets, keys, and credentials (`*.pem`, `*.key`, `.env`).
- Local tool configurations and session states.

If a change needs process or architectural documentation, write it under
`docs/` instead of committing local or private tooling artifacts.

## Release Gate

Before any release claim, maintainers verify all of the following:

- [ ] `git status` is clean except for the intended release changes.
- [ ] `python scripts/validate_templates.py --quiet` passes.
- [ ] `python scripts/validate_templates.py --selftest` passes.
- [ ] Every `.github/workflows/*.yml` file parses.
- [ ] Tracked Markdown relative links resolve.
- [ ] Tracked generated artifacts and private files are absent.
- [ ] Staged and tracked content has no obvious secret patterns.
- [ ] `git diff --check` passes.
- [ ] The intended commit is pushed and matches `origin/main`.
- [ ] GitHub Actions for the exact release commit pass.
- [ ] The release tag points to the same commit.

If any gate is unavailable, report `NOT_RUN` or `BLOCKED` with the exact scope
instead of weakening the claim.

## Contributor Checklist

Use this checklist for non-trivial template, CI, or documentation changes:

- [ ] Identify the affected starters, workflows, and docs.
- [ ] Keep the change atomic and idiomatic to its ecosystem.
- [ ] Run the validator and the affected starter's own commands.
- [ ] Update docs only where the contract, rationale, or navigation changed.
- [ ] Stage explicit public paths only; keep local configuration untracked.
- [ ] Commit with a Conventional Commit message
  (see [conventions](conventions.md)).
- [ ] Push, then verify exact-head GitHub Actions before calling the work
  complete.

## Related Documents

- [Maintainer guide](maintainer-guide.md) — Dependabot triage, branch hygiene,
  branch protection, release operations.
- [Conventions](conventions.md) — naming, commits, versioning, git workflow.
- [Verification matrix](verification-matrix.md) — per-starter evidence index.
- [Template specification](template-specification.md) — the baseline each
  starter must meet.

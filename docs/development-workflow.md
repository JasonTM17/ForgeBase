# Development and Verification Workflow

Languages: English | [Tiếng Việt](development-workflow.vi.md)

ForgeBase uses a structured, evidence-based engineering workflow to keep a large starter
catalog honest, reviewable, and reproducible. This document describes the standard process
governing template creation, maintenance, and verification.

> **Ghi chú tiếng Việt:** Tài liệu này mô tả quy trình kỹ thuật và tiêu chuẩn kiểm chứng
> của ForgeBase nhằm đảm bảo mọi starter đều đạt chuẩn production.

## Workflow

Every material change follows the same evidence path:

1. **Scout** the affected templates, docs, scripts, and CI workflow.
2. **Plan** the smallest coherent change and record the expected evidence.
3. **Implement** only the approved scope.
4. **Test** with the validator plus the affected ecosystem gates.
5. **Review** for spec compliance, security, portability, and verification gaps.
6. **Release** only after the repository state, commit, push, CI, and tag
   evidence all line up.

Small documentation-only changes may use a shorter path, but they still need a
clean diff, link checks, and no untracked/temporary files staged.
For repeatable repository operations, pair this workflow with the
[maintainer guide](maintainer-guide.md).

## Roles and Responsibilities

- **Author / Implementer** scopes the change, performs the implementation, runs local
  verification gates, and opens the pull request with honest evidence labels.
- **Reviewer** independently evaluates the proposed change for spec compliance, ecosystem
  idioms, security concerns, boundary constraints, and edge cases.
- **Maintainer** owns the final decision, checks GitHub Actions against the exact branch head,
  manages branch protection, merges changes, and tags releases.

Reviewer findings do not automatically expand scope. They become immediate
work only when they expose an in-scope defect, invalidate a release claim, or
block the current acceptance signal.

## Evidence Vocabulary

ForgeBase uses explicit evidence labels:

- `PASS`: the stated command, review, or external check succeeded on the named
  scope.
- `FAIL`: the check ran and found a defect.
- `NOT_RUN`: the check did not run; no pass is implied.
- `BLOCKED`: the check could not complete because a required tool, credential,
  service, or decision was unavailable.

Status claims in README files, pull requests, and release notes must use these
meanings. A local test pass does not prove GitHub Actions, Docker publishing,
device behavior, or production deployment.

## Clean Repository Boundaries

Maintainers and contributors must keep local development noise and secrets out of the published repository:

- Local editor/IDE settings (`.vscode/`, `.idea/`, etc.)
- Dependency trees and virtual environments (`node_modules/`, `.venv/`, `vendor/`)
- Build outputs, binaries, and caches (`dist/`, `build/`, `target/`, `.cache/`)
- Private secrets, keys, and credentials (`*.pem`, `*.key`, `.env`)
- Local tool configurations and session states

If a change requires process or architectural documentation, write it under `docs/` rather than committing local or private tooling artifacts.

## Release Gate

Before a release claim, maintainers verify:

- `git status` is clean except for the intended release changes.
- `python scripts/validate_templates.py --quiet` passes.
- `python scripts/validate_templates.py --selftest` passes.
- all `.github/workflows/*.yml` files parse.
- tracked Markdown relative links resolve.
- tracked generated artifacts and private files are absent.
- staged or tracked content has no obvious secret patterns.
- `git diff --check` passes.
- the intended commit is pushed and matches `origin/main`.
- GitHub Actions for the exact release commit pass.
- the release tag points to the same commit.

If any gate is unavailable, report `NOT_RUN` or `BLOCKED` with the exact scope
instead of weakening the claim.

## Maintainer Checklist

Use this checklist for non-trivial template, CI, or documentation changes:

- Identify the affected starter(s), workflow(s), and docs.
- Keep the change atomic and idiomatic to the ecosystem.
- Run the validator and the affected starter's own commands.
- Update docs only where the contract, rationale, or navigation changed.
- Stage explicit public paths only.
- Keep local/temporary configuration files untracked.
- Commit with a Conventional Commit message.
- Push, then verify exact-head GitHub Actions before calling the work complete.

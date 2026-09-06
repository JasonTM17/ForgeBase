# AgentKit Workflow

Languages: English | [Tiếng Việt](agentkit-workflow.vi.md)

ForgeBase uses an AgentKit-guided engineering workflow to keep a large starter
catalog honest, reviewable, and reproducible. This document describes the
public process. It does not publish private AgentKit runtime files, local skill
registries, prompts, or execution ledgers.

> **Ghi chú tiếng Việt:** Tài liệu này chỉ mô tả quy trình công khai của
> ForgeBase. Các file AgentKit cục bộ, skill registry, prompt, và execution
> ledger vẫn là private và không upload lên GitHub.

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
clean diff, link checks, and no private files staged.

## Roles

- **Controller** owns the final decision, edits, staged paths, commits, and
  push boundary.
- **Advisor** is used when outcome, scope, or trade-offs are ambiguous.
- **Kongming** reviews architecture, sequencing, and release readiness for
  higher-risk changes.
- **Wukong** tries to falsify one load-bearing claim, such as "this workflow
  proves every matrix entry" or "this template is self-contained."

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
  service, or user decision was unavailable.

Status claims in README files, pull requests, and release notes must use these
meanings. A local test pass does not prove GitHub Actions, Docker publishing,
device behavior, or production deployment.

## Public And Private Boundaries

Public repository documentation may describe the AK workflow and its gates.
Private AgentKit operating files stay out of the published repository:

- `.agentkit/`
- `.agents/`
- `.codex/`
- `AGENTS.md`
- `plans/`

These paths are intentionally ignored. If a change needs public process
documentation, write it under `docs/` instead of committing local runtime state.

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
- Keep private AgentKit runtime files untracked.
- Commit with a Conventional Commit message.
- Push, then verify exact-head GitHub Actions before calling the work complete.

# Maintainer Guide

Languages: English | [Tiếng Việt](maintainer-guide.vi.md)

This guide turns the [development workflow](development-workflow.md) into
day-to-day repository operations. It is written for maintainers handling
dependency updates, branch hygiene, release evidence, and repository settings.

## Operating principles

- Keep template changes small, idiomatic, and independently reviewable.
- Prefer one dependency-update group per ecosystem, matching
  `.github/dependabot.yml`.
- Record `PASS`, `FAIL`, `NOT_RUN`, and `BLOCKED` exactly as observed — see
  the evidence vocabulary in the [development workflow](development-workflow.md#evidence-vocabulary).
- Keep local runtime files, editor configurations, and caches out of public
  commits.
- Treat a local pass, a pushed branch, a GitHub Actions run, and a release tag
  as separate evidence boundaries.

## Dependabot triage

1. Fetch and inspect every open dependency branch before merging.
2. Read the changed manifests, lockfiles, and workflow files for that group.
3. Check upstream CI failures before assuming the update is bad; stale
   failures can come from earlier repository bugs that were since fixed.
4. Merge grouped updates only when the branch head is known and the affected
   gates have a verification path.
5. If a grouped update exposes a real incompatibility, fix the smallest
   dependency or template boundary that restores the supported runtime.

Useful commands:

```bash
git fetch --all --prune --tags
gh pr list --state open \
  --json number,title,headRefName,headRefOid,baseRefName,mergeStateStatus,statusCheckRollup
git merge-base --is-ancestor origin/<branch> HEAD
```

## Branch hygiene

Before deleting a remote branch, prove its head is already contained in the
intended base:

```bash
git merge-base --is-ancestor origin/<branch> origin/main
git rev-list --count origin/main..origin/<branch>
```

Only delete branches that return `ahead=0` and have no unmerged work. If the
proof is unavailable, keep the branch and report `NOT_RUN` or `BLOCKED`
instead of guessing.

## Main branch protection

`main` should be protected before a release is called complete. Recommended
settings:

- Require pull requests for changes to `main`.
- Require status checks only when they report reliably for the protected
  branch. With path-filtered workflows, do not require a check that can be
  skipped for unrelated PRs unless a ruleset, merge queue, or fan-in check
  keeps the required status stable.
- Disallow force pushes and branch deletion.
- Require conversation resolution before merge.
- Keep administrator bypass explicit and rare.
- Enable required code-owner reviews only after `.github/CODEOWNERS` reflects
  the ownership model maintainers actually want enforced.

When changing repository settings, record the date, the exact setting changed,
and whether the change was verified through the GitHub UI or API.

## Release evidence

Use this release sequence:

1. Verify the intended public diff and staged paths.
2. Run the repository gates:
   `python scripts/validate_templates.py --quiet`,
   `python scripts/validate_templates.py --selftest`,
   `python scripts/update_verification_matrix.py --check`,
   `python scripts/check_docs_links.py --quiet`, workflow YAML parsing,
   a secret scan, and `git diff --check`.
3. Run the affected ecosystem gates from the template README or workflow.
4. Push the exact commit.
5. Verify GitHub Actions for that exact commit.
6. Tag only after the commit, checks, documentation, and release notes agree.

Do not say "release-ready" when exact-head CI, a tag, provenance, or another
required external gate has not been observed.

## Documentation updates

Update docs when a change affects setup, supported runtime versions, commands,
CI behavior, verification evidence, repository policy, or maintainer workflow.
Do not duplicate long template README content into root docs; link to the
source of truth instead.

Keep English and Vietnamese documentation aligned in meaning — a translation
should stay faithful to the contract, even where the wording is not literal.

## Related documents

- [Development workflow](development-workflow.md) — the six-phase evidence
  path and release gate.
- [Conventions](conventions.md) — commits, versioning, and git workflow rules.
- [Verification matrix](verification-matrix.md) — generated per-starter
  evidence index.
